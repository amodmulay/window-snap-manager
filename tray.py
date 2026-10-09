"""System tray widget for Window Snap Manager."""

import logging
from typing import Callable, Dict

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

logger = logging.getLogger(__name__)


class TrayWidget:
    """System tray icon with snap layout menu."""

    def __init__(self, snap_callbacks: Dict[str, Callable]):
        """Initialize tray widget.

        Args:
            snap_callbacks: Dictionary of action -> callback functions
        """
        self.snap_callbacks = snap_callbacks
        self.icon = Gtk.StatusIcon()
        self.icon.set_from_icon_name("window-manager")
        self.icon.set_visible(True)
        self.icon.set_tooltip_text("Window Snap Manager")
        self.icon.connect("popup-menu", self._on_popup_menu)

    def _on_popup_menu(self, icon, button, activate_time):
        """Handle right-click menu."""
        menu = Gtk.Menu()

        # Quarters section
        quarters_item = Gtk.MenuItem(label="Quarters (2×2)")
        quarters_submenu = Gtk.Menu()
        self._add_menu_item(
            quarters_submenu, "Top Left", "quarter_top_left"
        )
        self._add_menu_item(
            quarters_submenu, "Top Right", "quarter_top_right"
        )
        self._add_menu_item(
            quarters_submenu, "Bottom Left", "quarter_bottom_left"
        )
        self._add_menu_item(
            quarters_submenu, "Bottom Right", "quarter_bottom_right"
        )
        self._add_menu_item(
            quarters_submenu, "Centered", "quarter_centered"
        )
        quarters_item.set_submenu(quarters_submenu)
        menu.append(quarters_item)

        # Thirds section
        thirds_item = Gtk.MenuItem(label="Thirds (1×3)")
        thirds_submenu = Gtk.Menu()
        self._add_menu_item(thirds_submenu, "Left", "third_left")
        self._add_menu_item(thirds_submenu, "Center", "third_center")
        self._add_menu_item(thirds_submenu, "Right", "third_right")
        thirds_item.set_submenu(thirds_submenu)
        menu.append(thirds_item)

        # Sixths section
        sixths_item = Gtk.MenuItem(label="Sixths (2×3)")
        sixths_submenu = Gtk.Menu()
        self._add_menu_item(sixths_submenu, "Top Left", "sixth_top_left")
        self._add_menu_item(
            sixths_submenu, "Top Center", "sixth_top_center"
        )
        self._add_menu_item(sixths_submenu, "Top Right", "sixth_top_right")
        self._add_menu_item(
            sixths_submenu, "Bottom Left", "sixth_bottom_left"
        )
        self._add_menu_item(
            sixths_submenu, "Bottom Center", "sixth_bottom_center"
        )
        self._add_menu_item(
            sixths_submenu, "Bottom Right", "sixth_bottom_right"
        )
        sixths_item.set_submenu(sixths_submenu)
        menu.append(sixths_item)

        # Ninths section
        ninths_item = Gtk.MenuItem(label="Ninths (3×3)")
        ninths_submenu = Gtk.Menu()
        self._add_menu_item(ninths_submenu, "Top Left", "ninth_top_left")
        self._add_menu_item(ninths_submenu, "Top Center", "ninth_top_center")
        self._add_menu_item(ninths_submenu, "Top Right", "ninth_top_right")
        self._add_menu_item(
            ninths_submenu, "Middle Left", "ninth_middle_left"
        )
        self._add_menu_item(
            ninths_submenu, "Middle Center", "ninth_middle_center"
        )
        self._add_menu_item(
            ninths_submenu, "Middle Right", "ninth_middle_right"
        )
        self._add_menu_item(ninths_submenu, "Bottom Left", "ninth_bottom_left")
        self._add_menu_item(
            ninths_submenu, "Bottom Center", "ninth_bottom_center"
        )
        self._add_menu_item(
            ninths_submenu, "Bottom Right", "ninth_bottom_right"
        )
        ninths_item.set_submenu(ninths_submenu)
        menu.append(ninths_item)

        # Halves section
        halves_item = Gtk.MenuItem(label="Halves (1×2)")
        halves_submenu = Gtk.Menu()
        self._add_menu_item(halves_submenu, "Left", "half_left")
        self._add_menu_item(halves_submenu, "Right", "half_right")
        self._add_menu_item(halves_submenu, "Top", "half_top")
        self._add_menu_item(halves_submenu, "Bottom", "half_bottom")
        self._add_menu_item(
            halves_submenu, "Center Vertical", "half_center_vertical"
        )
        self._add_menu_item(
            halves_submenu, "Center Horizontal", "half_center_horizontal"
        )
        halves_item.set_submenu(halves_submenu)
        menu.append(halves_item)

        # Two Thirds section
        two_thirds_item = Gtk.MenuItem(label="Two Thirds")
        two_thirds_submenu = Gtk.Menu()
        self._add_menu_item(two_thirds_submenu, "Left", "two_thirds_left")
        self._add_menu_item(
            two_thirds_submenu, "Center", "two_thirds_center"
        )
        self._add_menu_item(two_thirds_submenu, "Right", "two_thirds_right")
        two_thirds_item.set_submenu(two_thirds_submenu)
        menu.append(two_thirds_item)

        # Separator
        menu.append(Gtk.SeparatorMenuItem())

        # Other options
        self._add_menu_item(menu, "Center", "center")
        self._add_menu_item(menu, "Maximize", "maximize")

        # Separator
        menu.append(Gtk.SeparatorMenuItem())

        # Exit option
        exit_item = Gtk.MenuItem(label="Exit")
        exit_item.connect("activate", self._on_exit)
        menu.append(exit_item)

        menu.show_all()
        menu.popup_at_pointer(None)

    def _add_menu_item(self, menu: Gtk.Menu, label: str, action: str):
        """Add a menu item that calls a snap callback."""
        item = Gtk.MenuItem(label=label)
        if action in self.snap_callbacks:
            item.connect("activate", lambda w: self.snap_callbacks[action]())
        else:
            item.set_sensitive(False)
        menu.append(item)

    def _on_exit(self, widget):
        """Handle exit menu item."""
        Gtk.main_quit()
