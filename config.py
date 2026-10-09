"""Configuration management for shortcuts."""

import json
import logging
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)

# Default config directory
CONFIG_DIR = Path.home() / ".config" / "window-snap-manager"
CONFIG_FILE = CONFIG_DIR / "config.json"


def ensure_config_dir():
    """Create config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def get_default_shortcuts() -> Dict[str, str]:
    """Get default keyboard shortcuts."""
    return {
        # Quarters
        "quarter_top_left": "<Super>ctrl+u",
        "quarter_top_right": "<Super>ctrl+i",
        "quarter_bottom_left": "<Super>ctrl+j",
        "quarter_bottom_right": "<Super>ctrl+k",
        "quarter_centered": "<Super>ctrl+alt+c",
        # Thirds
        "third_left": "<Super>ctrl+d",
        "third_center": "<Super>ctrl+f",
        "third_right": "<Super>ctrl+g",
        # Sixths
        "sixth_top_left": "<Super>ctrl+shift+u",
        "sixth_top_center": "<Super>ctrl+shift+i",
        "sixth_top_right": "<Super>ctrl+shift+o",
        "sixth_bottom_left": "<Super>ctrl+shift+j",
        "sixth_bottom_center": "<Super>ctrl+shift+k",
        "sixth_bottom_right": "<Super>ctrl+shift+l",
        # Ninths
        "ninth_top_left": "<Super>ctrl+alt+u",
        "ninth_top_center": "<Super>ctrl+alt+i",
        "ninth_top_right": "<Super>ctrl+alt+o",
        "ninth_middle_left": "<Super>ctrl+alt+j",
        "ninth_middle_center": "<Super>ctrl+alt+k",
        "ninth_middle_right": "<Super>ctrl+alt+l",
        "ninth_bottom_left": "<Super>ctrl+alt+n",
        "ninth_bottom_center": "<Super>ctrl+alt+m",
        "ninth_bottom_right": "<Super>ctrl+alt+comma",
        # Halves
        "half_left": "<Super>ctrl+Left",
        "half_right": "<Super>ctrl+Right",
        "half_top": "<Super>ctrl+Up",
        "half_bottom": "<Super>ctrl+Down",
        "half_center_vertical": "<Super>ctrl+shift+c",
        "half_center_horizontal": "<Super>ctrl+shift+v",
        # Two Thirds
        "two_thirds_left": "<Super>ctrl+e",
        "two_thirds_center": "<Super>ctrl+r",
        "two_thirds_right": "<Super>ctrl+t",
        # Center
        "center": "<Super>ctrl+c",
        # Maximize
        "maximize": "<Super>ctrl+Return",
    }


def load_config() -> Dict[str, str]:
    """Load shortcuts from config file."""
    ensure_config_dir()

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
            logger.info(f"Loaded config from {CONFIG_FILE}")
            return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")

    # Return defaults if no config exists
    return get_default_shortcuts()


def save_config(config: Dict[str, str]) -> bool:
    """Save shortcuts to config file."""
    ensure_config_dir()
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        logger.info(f"Saved config to {CONFIG_FILE}")
        return True
    except Exception as e:
        logger.error(f"Failed to save config: {e}")
        return False


def get_shortcut(action: str) -> str:
    """Get shortcut for an action."""
    config = load_config()
    return config.get(action, "")
