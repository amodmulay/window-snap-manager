"""Keyboard shortcut registration and handling."""

import logging
from typing import Callable, Dict

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

logger = logging.getLogger(__name__)


class ShortcutManager:
    """Register and handle global keyboard shortcuts."""

    def __init__(self):
        self.shortcuts: Dict[str, Callable] = {}
        self.display = Gdk.Display.get_default()
        self.seat = self.display.get_default_seat()
        self.keyboard = self.seat.get_pointer()  # Get keyboard from seat

    def register(self, shortcut: str, callback: Callable) -> bool:
        """Register a global keyboard shortcut.

        Args:
            shortcut: Keybinding string (e.g., "<Super>Ctrl+U")
            callback: Function to call when shortcut is pressed
        """
        try:
            # Parse the shortcut
            key, mods = Gtk.accelerator_parse(shortcut)
            if key == 0:
                logger.error(f"Invalid shortcut: {shortcut}")
                return False

            self.shortcuts[shortcut] = callback
            logger.info(f"Registered shortcut: {shortcut}")
            return True
        except Exception as e:
            logger.error(f"Failed to register shortcut {shortcut}: {e}")
            return False

    def unregister(self, shortcut: str) -> bool:
        """Unregister a keyboard shortcut."""
        if shortcut in self.shortcuts:
            del self.shortcuts[shortcut]
            logger.info(f"Unregistered shortcut: {shortcut}")
            return True
        return False

    def get_all_shortcuts(self) -> Dict[str, Callable]:
        """Get all registered shortcuts."""
        return self.shortcuts.copy()
