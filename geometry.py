"""Grid-based window geometry calculations."""

from dataclasses import dataclass


@dataclass
class Rect:
    """Window rectangle with x, y, width, height."""
    x: int
    y: int
    width: int
    height: int


@dataclass
class Monitor:
    """Monitor with geometry."""
    x: int
    y: int
    width: int
    height: int


class GridCalculator:
    """Calculate snap positions based on grid layouts."""

    @staticmethod
    def quarter(monitor: Monitor, position: str) -> Rect:
        """Get quarter screen position (2x2 grid)."""
        w = monitor.width // 2
        h = monitor.height // 2
        positions = {
            "top_left": (monitor.x, monitor.y),
            "top_right": (monitor.x + w, monitor.y),
            "bottom_left": (monitor.x, monitor.y + h),
            "bottom_right": (monitor.x + w, monitor.y + h),
        }
        x, y = positions[position]
        return Rect(x, y, w, h)

    @staticmethod
    def quarter_centered(monitor: Monitor) -> Rect:
        """Get centered quarter (50% width/height, centered)."""
        w = monitor.width // 2
        h = monitor.height // 2
        x = monitor.x + (monitor.width - w) // 2
        y = monitor.y + (monitor.height - h) // 2
        return Rect(x, y, w, h)

    @staticmethod
    def third(monitor: Monitor, position: str) -> Rect:
        """Get third screen position (1x3 grid - left/center/right)."""
        w = monitor.width // 3
        h = monitor.height
        positions = {
            "left": (monitor.x, monitor.y),
            "center": (monitor.x + w, monitor.y),
            "right": (monitor.x + 2 * w, monitor.y),
        }
        x, y = positions[position]
        return Rect(x, y, w, h)

    @staticmethod
    def sixth(monitor: Monitor, position: str) -> Rect:
        """Get sixth screen position (2x3 grid)."""
        w = monitor.width // 3
        h = monitor.height // 2
        positions = {
            "top_left": (monitor.x, monitor.y),
            "top_center": (monitor.x + w, monitor.y),
            "top_right": (monitor.x + 2 * w, monitor.y),
            "bottom_left": (monitor.x, monitor.y + h),
            "bottom_center": (monitor.x + w, monitor.y + h),
            "bottom_right": (monitor.x + 2 * w, monitor.y + h),
        }
        x, y = positions[position]
        return Rect(x, y, w, h)

    @staticmethod
    def ninth(monitor: Monitor, position: str) -> Rect:
        """Get ninth screen position (3x3 grid)."""
        w = monitor.width // 3
        h = monitor.height // 3
        positions = {
            "top_left": (monitor.x, monitor.y),
            "top_center": (monitor.x + w, monitor.y),
            "top_right": (monitor.x + 2 * w, monitor.y),
            "middle_left": (monitor.x, monitor.y + h),
            "middle_center": (monitor.x + w, monitor.y + h),
            "middle_right": (monitor.x + 2 * w, monitor.y + h),
            "bottom_left": (monitor.x, monitor.y + 2 * h),
            "bottom_center": (monitor.x + w, monitor.y + 2 * h),
            "bottom_right": (monitor.x + 2 * w, monitor.y + 2 * h),
        }
        x, y = positions[position]
        return Rect(x, y, w, h)

    @staticmethod
    def half(monitor: Monitor, position: str) -> Rect:
        """Get half screen position."""
        h = monitor.height
        w = monitor.width
        positions = {
            "left": (monitor.x, monitor.y, w // 2, h),
            "right": (monitor.x + w // 2, monitor.y, w // 2, h),
            "top": (monitor.x, monitor.y, w, h // 2),
            "bottom": (monitor.x, monitor.y + h // 2, w, h // 2),
            "center_vertical": (monitor.x + w // 4, monitor.y, w // 2, h),
            "center_horizontal": (monitor.x, monitor.y + h // 4, w, h // 2),
        }
        x, y, rw, rh = positions[position]
        return Rect(x, y, rw, rh)

    @staticmethod
    def two_thirds(monitor: Monitor, position: str) -> Rect:
        """Get two-thirds screen position."""
        w = (monitor.width * 2) // 3
        h = monitor.height
        third_w = monitor.width // 3
        positions = {
            "left": (monitor.x, monitor.y, w, h),
            "center": (monitor.x + third_w // 2, monitor.y, w, h),
            "right": (monitor.x + monitor.width - w, monitor.y, w, h),
        }
        x, y, rw, rh = positions[position]
        return Rect(x, y, rw, rh)

    @staticmethod
    def center(monitor: Monitor) -> Rect:
        """Get centered window (90% of screen, centered)."""
        w = (monitor.width * 9) // 10
        h = (monitor.height * 9) // 10
        x = monitor.x + (monitor.width - w) // 2
        y = monitor.y + (monitor.height - h) // 2
        return Rect(x, y, w, h)

    @staticmethod
    def maximize(monitor: Monitor) -> Rect:
        """Get full screen."""
        return Rect(monitor.x, monitor.y, monitor.width, monitor.height)
