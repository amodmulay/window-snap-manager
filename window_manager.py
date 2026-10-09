"""Wayland/GNOME window management via D-Bus."""

import logging
from typing import Optional

import dbus
from geometry import Monitor, Rect

logger = logging.getLogger(__name__)


class WaylandWindowManager:
    """Manage windows on Wayland via GNOME Shell D-Bus API."""

    def __init__(self):
        self.bus = dbus.SessionBus()
        self.shell_obj = self.bus.get_object(
            "org.gnome.Shell", "/org/gnome/Shell"
        )
        self.shell = dbus.Interface(self.shell_obj, "org.gnome.Shell")

    def get_active_window(self):
        """Get the currently focused window."""
        try:
            display = self.shell.Eval(
                "global.display.get_focus_window()"
            )
            return display
        except Exception as e:
            logger.error(f"Failed to get active window: {e}")
            return None

    def get_active_window_rect(self) -> Optional[Rect]:
        """Get the active window's current rectangle."""
        try:
            result = self.shell.Eval(
                "const w = global.display.get_focus_window(); "
                "w ? [w.get_buffer_rect().x, w.get_buffer_rect().y, "
                "w.get_buffer_rect().width, w.get_buffer_rect().height] : null"
            )
            if result and len(result) == 4:
                return Rect(*result)
        except Exception as e:
            logger.error(f"Failed to get window rect: {e}")
        return None

    def get_monitor_for_window(self) -> Optional[Monitor]:
        """Get the monitor geometry for the active window."""
        try:
            result = self.shell.Eval(
                "const w = global.display.get_focus_window(); "
                "const m = w.get_monitor(); "
                "const g = global.display.get_monitor_geometry(m); "
                "[g.x, g.y, g.width, g.height]"
            )
            if result and len(result) == 4:
                return Monitor(*result)
        except Exception as e:
            logger.error(f"Failed to get monitor geometry: {e}")
        return None

    def snap_window(self, rect: Rect) -> bool:
        """Snap active window to given rectangle."""
        try:
            js_code = (
                f"const w = global.display.get_focus_window(); "
                f"w.move_resize_frame(false, {rect.x}, {rect.y}, "
                f"{rect.width}, {rect.height});"
            )
            self.shell.Eval(js_code)
            logger.info(
                f"Snapped window to {rect.x}, {rect.y}, "
                f"{rect.width}x{rect.height}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to snap window: {e}")
            return False
