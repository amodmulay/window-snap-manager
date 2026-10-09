#!/usr/bin/env python3
"""Window Snap Manager - A Rectangle-like window snapping tool for Ubuntu/Wayland."""

import logging
import signal
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from config import load_config
from geometry import GridCalculator
from shortcuts import ShortcutManager
from window_manager import WaylandWindowManager
from tray import TrayWidget

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class WindowSnapManager:
    """Main application coordinator."""

    def __init__(self):
        self.wm = WaylandWindowManager()
        self.shortcuts = ShortcutManager()
        self.config = load_config()
        self.grid = GridCalculator()
        self.running = True
        self.tray = None
        self.snap_callbacks = {}

    def snap_quarter(self, position: str) -> bool:
        """Snap to quarter position."""
        monitor = self.wm.get_monitor_for_window()
        if not monitor:
            logger.error("Could not get monitor geometry")
            return False

        if position == "centered":
            rect = self.grid.quarter_centered(monitor)
        else:
            rect = self.grid.quarter(monitor, position)

        return self.wm.snap_window(rect)

    def snap_third(self, position: str) -> bool:
        """Snap to third position."""
        monitor = self.wm.get_monitor_for_window()
        if not monitor:
            logger.error("Could not get monitor geometry")
            return False
        rect = self.grid.third(monitor, position)
        return self.wm.snap_window(rect)

    def snap_sixth(self, position: str) -> bool:
        """Snap to sixth position."""
        monitor = self.wm.get_monitor_for_window()
        if not monitor:
            logger.error("Could not get monitor geometry")
            return False
        rect = self.grid.sixth(monitor, position)
        return self.wm.snap_window(rect)

    def snap_ninth(self, position: str) -> bool:
        """Snap to ninth position."""
        monitor = self.wm.get_monitor_for_window()
        if not monitor:
            logger.error("Could not get monitor geometry")
            return False
        rect = self.grid.ninth(monitor, position)
        return self.wm.snap_window(rect)

    def snap_half(self, position: str) -> bool:
        """Snap to half position."""
        monitor = self.wm.get_monitor_for_window()
        if not monitor:
            logger.error("Could not get monitor geometry")
            return False
        rect = self.grid.half(monitor, position)
        return self.wm.snap_window(rect)

    def snap_two_thirds(self, position: str) -> bool:
        """Snap to two-thirds position."""
        monitor = self.wm.get_monitor_for_window()
        if not monitor:
            logger.error("Could not get monitor geometry")
            return False
        rect = self.grid.two_thirds(monitor, position)
        return self.wm.snap_window(rect)

    def snap_center(self) -> bool:
        """Snap to center."""
        monitor = self.wm.get_monitor_for_window()
        if not monitor:
            logger.error("Could not get monitor geometry")
            return False
        rect = self.grid.center(monitor)
        return self.wm.snap_window(rect)

    def snap_maximize(self) -> bool:
        """Maximize window."""
        monitor = self.wm.get_monitor_for_window()
        if not monitor:
            logger.error("Could not get monitor geometry")
            return False
        rect = self.grid.maximize(monitor)
        return self.wm.snap_window(rect)

    def setup_callbacks(self):
        """Set up snap callbacks for both keyboard and tray."""
        self.snap_callbacks = {
            "quarter_top_left": lambda: self.snap_quarter("top_left"),
            "quarter_top_right": lambda: self.snap_quarter("top_right"),
            "quarter_bottom_left": lambda: self.snap_quarter("bottom_left"),
            "quarter_bottom_right": lambda: self.snap_quarter("bottom_right"),
            "quarter_centered": lambda: self.snap_quarter("centered"),
            "third_left": lambda: self.snap_third("left"),
            "third_center": lambda: self.snap_third("center"),
            "third_right": lambda: self.snap_third("right"),
            "sixth_top_left": lambda: self.snap_sixth("top_left"),
            "sixth_top_center": lambda: self.snap_sixth("top_center"),
            "sixth_top_right": lambda: self.snap_sixth("top_right"),
            "sixth_bottom_left": lambda: self.snap_sixth("bottom_left"),
            "sixth_bottom_center": lambda: self.snap_sixth("bottom_center"),
            "sixth_bottom_right": lambda: self.snap_sixth("bottom_right"),
            "ninth_top_left": lambda: self.snap_ninth("top_left"),
            "ninth_top_center": lambda: self.snap_ninth("top_center"),
            "ninth_top_right": lambda: self.snap_ninth("top_right"),
            "ninth_middle_left": lambda: self.snap_ninth("middle_left"),
            "ninth_middle_center": lambda: self.snap_ninth("middle_center"),
            "ninth_middle_right": lambda: self.snap_ninth("middle_right"),
            "ninth_bottom_left": lambda: self.snap_ninth("bottom_left"),
            "ninth_bottom_center": lambda: self.snap_ninth("bottom_center"),
            "ninth_bottom_right": lambda: self.snap_ninth("bottom_right"),
            "half_left": lambda: self.snap_half("left"),
            "half_right": lambda: self.snap_half("right"),
            "half_top": lambda: self.snap_half("top"),
            "half_bottom": lambda: self.snap_half("bottom"),
            "half_center_vertical": lambda: self.snap_half("center_vertical"),
            "half_center_horizontal": lambda: self.snap_half("center_horizontal"),
            "two_thirds_left": lambda: self.snap_two_thirds("left"),
            "two_thirds_center": lambda: self.snap_two_thirds("center"),
            "two_thirds_right": lambda: self.snap_two_thirds("right"),
            "center": lambda: self.snap_center(),
            "maximize": lambda: self.snap_maximize(),
        }

    def register_shortcuts(self):
        """Register all keyboard shortcuts."""
        for action, callback in self.snap_callbacks.items():
            shortcut = self.config.get(action)
            if shortcut:
                self.shortcuts.register(shortcut, callback)
            else:
                logger.warning(f"No shortcut configured for action: {action}")

    def run(self):
        """Run the application."""
        logger.info("Starting Window Snap Manager")

        self.setup_callbacks()
        self.register_shortcuts()
        self.shortcuts.start()

        # Create system tray widget
        self.tray = TrayWidget(self.snap_callbacks)
        logger.info("System tray widget created")

        # Set up signal handlers
        def handle_signal(signum, frame):
            logger.info("Received signal, shutting down")
            self.running = False
            self.shortcuts.stop()
            Gtk.main_quit()

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        logger.info("Window Snap Manager running. Press Ctrl+C to exit.")
        try:
            Gtk.main()
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            self.shortcuts.stop()


def main():
    """Entry point."""
    app = WindowSnapManager()
    app.run()


if __name__ == "__main__":
    main()
