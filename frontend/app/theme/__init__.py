"""Design System - Theme."""

from .colors import ColorPalette, DarkColorPalette, dark_colors, get_colors, light_colors
from .spacing import (
    COMPONENT_SPACING,
    GRID_COLUMNS,
    GRID_GAP,
    BorderRadius,
    Breakpoint,
    Size,
    Spacing,
    ZIndex,
    border_radius,
    breakpoint,
    size,
    spacing,
    z_index,
)
from .typography import (
    BODY_STYLES,
    BUTTON_STYLES,
    HEADING_STYLES,
    FontSize,
    FontWeight,
    LetterSpacing,
    LineHeight,
    Typography,
    typography,
)

__all__ = [
    # Colors
    "ColorPalette",
    "DarkColorPalette",
    "light_colors",
    "dark_colors",
    "get_colors",
    # Typography
    "Typography",
    "FontSize",
    "FontWeight",
    "LineHeight",
    "LetterSpacing",
    "typography",
    "HEADING_STYLES",
    "BODY_STYLES",
    "BUTTON_STYLES",
    # Spacing
    "Spacing",
    "BorderRadius",
    "Size",
    "ZIndex",
    "Breakpoint",
    "spacing",
    "border_radius",
    "size",
    "z_index",
    "breakpoint",
    "GRID_COLUMNS",
    "GRID_GAP",
    "COMPONENT_SPACING",
]
