# Window Snap Manager

A window snapping manager for Ubuntu/GNOME Wayland, similar to Rectangle on macOS.

## Features

- **Quarter snapping** (2x2 grid)
- **Third snapping** (1x3 grid - left/center/right)
- **Sixth snapping** (2x3 grid)
- **Ninth snapping** (3x3 grid)
- **Half snapping** (left/right/top/bottom/center)
- **Two-thirds snapping**
- **Center snapping**
- **Maximize**
- Fully configurable keyboard shortcuts

## Requirements

- Python 3.10+
- Ubuntu 20.04+ with GNOME on Wayland
- D-Bus (usually installed by default)

## Installation

1. Clone the repository:
```bash
cd ~/window-snap-manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python3 main.py
```

## Default Keyboard Shortcuts

### Quarters (2x2 Grid)
- `Super+Ctrl+U` - Top Left
- `Super+Ctrl+I` - Top Right
- `Super+Ctrl+J` - Bottom Left
- `Super+Ctrl+K` - Bottom Right
- `Super+Ctrl+Alt+C` - Centered

### Thirds (1x3 Grid)
- `Super+Ctrl+D` - Left
- `Super+Ctrl+F` - Center
- `Super+Ctrl+G` - Right

### Sixths (2x3 Grid)
- `Super+Ctrl+Shift+U` - Top Left
- `Super+Ctrl+Shift+I` - Top Center
- `Super+Ctrl+Shift+O` - Top Right
- `Super+Ctrl+Shift+J` - Bottom Left
- `Super+Ctrl+Shift+K` - Bottom Center
- `Super+Ctrl+Shift+L` - Bottom Right

### Ninths (3x3 Grid)
- `Super+Ctrl+Alt+U` - Top Left
- `Super+Ctrl+Alt+I` - Top Center
- `Super+Ctrl+Alt+O` - Top Right
- `Super+Ctrl+Alt+J` - Middle Left
- `Super+Ctrl+Alt+K` - Middle Center
- `Super+Ctrl+Alt+L` - Middle Right
- `Super+Ctrl+Alt+N` - Bottom Left
- `Super+Ctrl+Alt+M` - Bottom Center
- `Super+Ctrl+Alt+,` - Bottom Right

### Halves
- `Super+Ctrl+Left` - Left
- `Super+Ctrl+Right` - Right
- `Super+Ctrl+Up` - Top
- `Super+Ctrl+Down` - Bottom
- `Super+Ctrl+Shift+C` - Center Vertical
- `Super+Ctrl+Shift+V` - Center Horizontal

### Two Thirds
- `Super+Ctrl+E` - Left
- `Super+Ctrl+R` - Center
- `Super+Ctrl+T` - Right

### Other
- `Super+Ctrl+C` - Center
- `Super+Ctrl+Return` - Maximize

## Configuration

Shortcuts are stored in `~/.config/window-snap-manager/config.json`. You can edit this file directly to customize shortcuts.

## Architecture

- **`main.py`** - Main application coordinator
- **`window_manager.py`** - Wayland/GNOME window management via D-Bus
- **`geometry.py`** - Grid-based window geometry calculations
- **`shortcuts.py`** - Keyboard shortcut registration and handling
- **`config.py`** - Configuration management

## Notes

- Requires GNOME Shell D-Bus API access
- Works only on Wayland (not X11)
- Some shortcuts may conflict with system shortcuts, adjust in config
