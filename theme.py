# This file centralizes every color and font reference from our design system,
# so the rest of the UI code never hardcodes a hex value directly.
# If the design changes later, we only need to update it here.

# --- Colors (from DESIGN.md) ---

COLOR_SURFACE = "#f8f9fa"
COLOR_SURFACE_CONTAINER_LOW = "#f3f4f5"
COLOR_SURFACE_CONTAINER = "#edeeef"
COLOR_SURFACE_CONTAINER_HIGH = "#e7e8e9"
COLOR_ON_SURFACE = "#191c1d"
COLOR_ON_SURFACE_VARIANT = "#42474a"
COLOR_OUTLINE = "#73787b"
COLOR_OUTLINE_VARIANT = "#c2c7ca"

# Primary - Slate Gray, used for stable/calm elements (4+ days left)
COLOR_PRIMARY = "#2e434c"
COLOR_PRIMARY_CONTAINER = "#455a64"
COLOR_ON_PRIMARY = "#ffffff"

# Secondary - Crimson Red, used for urgency/destructive actions (today/1 day left)
COLOR_SECONDARY = "#b6171e"
COLOR_SECONDARY_CONTAINER = "#da3433"
COLOR_ON_SECONDARY = "#ffffff"

# Tertiary - Amber/Orange, used for mid-range caution (2-3 days left)
COLOR_TERTIARY = "#673000"
COLOR_TERTIARY_CONTAINER = "#8a4300"
COLOR_ON_TERTIARY = "#ffffff"

# Error (used interchangeably with secondary in some contexts)
COLOR_ERROR = "#ba1a1a"
COLOR_ERROR_CONTAINER = "#ffdad6"


def get_urgency_color(days_left: int) -> str:
    """
    Returns the appropriate color hex string based on how many days
    are left before an email is deleted. This is the core function
    that drives our 'urgent stuff looks loud, calm stuff looks calm' rule.
    """
    if days_left <= 1:
        # Today or 1 day left - critical, use red
        return COLOR_SECONDARY_CONTAINER
    elif days_left <= 3:
        # 2-3 days left - moderate caution, use amber
        return COLOR_TERTIARY_CONTAINER
    else:
        # 4+ days left - calm, use slate gray
        return COLOR_PRIMARY_CONTAINER


def get_urgency_label(days_left: int) -> str:
    """
    Returns the human readable urgency text shown on each card,
    e.g. 'TODAY', '1 DAY LEFT', '5 DAYS LEFT'.
    """
    if days_left <= 0:
        return "TODAY"
    elif days_left == 1:
        return "1 DAY LEFT"
    else:
        return f"{days_left} DAYS LEFT"


# --- Fonts ---
# These are registered with Kivy's font system in main.py at startup.
# We just define the friendly names here so other files can reference
# them consistently.

FONT_HEADING = "HankenGrotesk"
FONT_BODY = "HankenGrotesk"
FONT_MONO = "JetBrainsMono"
