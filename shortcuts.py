"""Global keyboard shortcut handling using pynput."""

import logging
import threading
from typing import Callable, Dict
from pynput import keyboard

logger = logging.getLogger(__name__)


class ShortcutManager:
    """Listen for and handle global keyboard shortcuts."""

    def __init__(self):
        self.shortcuts: Dict[tuple, Callable] = {}
        self.listener = None
        self.pressed_keys = set()

    def _parse_shortcut(self, shortcut_str: str) -> tuple:
        """Parse shortcut string into key tuple.

        Examples:
            "<Super>ctrl+u" -> (keyboard.Key.cmd, keyboard.KeyCode(char='u'), True)
            "<Super>ctrl+Left" -> (keyboard.Key.cmd, keyboard.Key.left, True)
        """
        parts = shortcut_str.lower().replace("<super>", "").split("+")
        keys = []

        for part in parts:
            part = part.strip()
            if part == "ctrl":
                keys.append("ctrl")
            elif part == "alt":
                keys.append("alt")
            elif part == "shift":
                keys.append("shift")
            elif part == "left":
                keys.append(keyboard.Key.left)
            elif part == "right":
                keys.append(keyboard.Key.right)
            elif part == "up":
                keys.append(keyboard.Key.up)
            elif part == "down":
                keys.append(keyboard.Key.down)
            elif part == "return":
                keys.append(keyboard.Key.enter)
            elif part == "comma":
                keys.append(keyboard.Key.comma)
            else:
                try:
                    keys.append(keyboard.KeyCode(char=part))
                except Exception:
                    logger.warning(f"Unknown key in shortcut: {part}")

        return tuple(keys)

    def register(self, shortcut: str, callback: Callable) -> bool:
        """Register a global keyboard shortcut.

        Args:
            shortcut: Keybinding string (e.g., "<Super>ctrl+u")
            callback: Function to call when shortcut is pressed
        """
        try:
            key_tuple = self._parse_shortcut(shortcut)
            self.shortcuts[key_tuple] = callback
            logger.info(f"Registered shortcut: {shortcut}")
            return True
        except Exception as e:
            logger.error(f"Failed to register shortcut {shortcut}: {e}")
            return False

    def unregister(self, shortcut: str) -> bool:
        """Unregister a keyboard shortcut."""
        try:
            key_tuple = self._parse_shortcut(shortcut)
            if key_tuple in self.shortcuts:
                del self.shortcuts[key_tuple]
                logger.info(f"Unregistered shortcut: {shortcut}")
                return True
        except Exception as e:
            logger.error(f"Failed to unregister shortcut: {e}")
        return False

    def _on_press(self, key):
        """Handle key press events."""
        self.pressed_keys.add(key)
        self._check_shortcuts()

    def _on_release(self, key):
        """Handle key release events."""
        self.pressed_keys.discard(key)

    def _check_shortcuts(self):
        """Check if any registered shortcut is pressed."""
        for key_combo, callback in self.shortcuts.items():
            if self._matches_combo(key_combo):
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Error executing shortcut callback: {e}")

    def _matches_combo(self, combo: tuple) -> bool:
        """Check if pressed keys match a shortcut combo."""
        required_modifiers = {"ctrl": False, "alt": False, "shift": False}
        required_key = None

        for key in combo:
            if key == "ctrl":
                required_modifiers["ctrl"] = True
            elif key == "alt":
                required_modifiers["alt"] = True
            elif key == "shift":
                required_modifiers["shift"] = True
            else:
                required_key = key

        # Check modifiers
        ctrl_pressed = any(
            k == keyboard.Key.ctrl_l or k == keyboard.Key.ctrl_r
            for k in self.pressed_keys
        )
        alt_pressed = any(
            k == keyboard.Key.alt_l or k == keyboard.Key.alt_r
            for k in self.pressed_keys
        )
        shift_pressed = any(
            k == keyboard.Key.shift_l or k == keyboard.Key.shift_r
            for k in self.pressed_keys
        )

        # Check if modifier requirements match
        if required_modifiers["ctrl"] != ctrl_pressed:
            return False
        if required_modifiers["alt"] != alt_pressed:
            return False
        if required_modifiers["shift"] != shift_pressed:
            return False

        # Check main key
        if required_key:
            return required_key in self.pressed_keys

        return True

    def start(self):
        """Start listening for keyboard events."""
        if self.listener is None:
            self.listener = keyboard.Listener(
                on_press=self._on_press, on_release=self._on_release
            )
            self.listener.daemon = True
            self.listener.start()
            logger.info("Keyboard listener started")

    def stop(self):
        """Stop listening for keyboard events."""
        if self.listener:
            self.listener.stop()
            self.listener = None
            logger.info("Keyboard listener stopped")

    def get_all_shortcuts(self) -> Dict:
        """Get all registered shortcuts."""
        return self.shortcuts.copy()
