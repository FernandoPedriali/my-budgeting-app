"""Design System - Typography."""

from dataclasses import dataclass, field


@dataclass
class FontSize:
    """Tamanhos de fonte."""

    xs: str = "0.75rem"  # 12px
    sm: str = "0.875rem"  # 14px
    base: str = "1rem"  # 16px
    lg: str = "1.125rem"  # 18px
    xl: str = "1.25rem"  # 20px
    xl2: str = "1.5rem"  # 24px
    xl3: str = "1.875rem"  # 30px
    xl4: str = "2.25rem"  # 36px
    xl5: str = "3rem"  # 48px


@dataclass
class FontWeight:
    """Pesos de fonte."""

    light: int = 300
    regular: int = 400
    medium: int = 500
    semibold: int = 600
    bold: int = 700
    extrabold: int = 800


@dataclass
class LineHeight:
    """Alturas de linha."""

    none: str = "1"
    tight: str = "1.25"
    snug: str = "1.375"
    normal: str = "1.5"
    relaxed: str = "1.625"
    loose: str = "2"


@dataclass
class LetterSpacing:
    """Espaçamento entre letras."""

    tighter: str = "-0.05em"
    tight: str = "-0.025em"
    normal: str = "0"
    wide: str = "0.025em"
    wider: str = "0.05em"
    widest: str = "0.1em"


@dataclass
class Typography:
    """Sistema de tipografia."""

    # Font Families
    sans: str = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    mono: str = "ui-monospace, SFMono-Regular, 'SF Mono', Consolas, 'Liberation Mono', monospace"

    # Tamanhos
    # 🔧 FIX: Usar field(default_factory=...) para evitar mutable default error
    size: FontSize = field(default_factory=FontSize)

    # Pesos
    weight: FontWeight = field(default_factory=FontWeight)

    # Line Heights
    line_height: LineHeight = field(default_factory=LineHeight)

    # Letter Spacing
    letter_spacing: LetterSpacing = field(default_factory=LetterSpacing)


# Instância global
typography = Typography()


# Estilos pré-definidos para elementos comuns
HEADING_STYLES = {
    "h1": {
        "font_size": typography.size.xl4,
        "font_weight": typography.weight.bold,
        "line_height": typography.line_height.tight,
        "letter_spacing": typography.letter_spacing.tight,
    },
    "h2": {
        "font_size": typography.size.xl3,
        "font_weight": typography.weight.bold,
        "line_height": typography.line_height.tight,
        "letter_spacing": typography.letter_spacing.tight,
    },
    "h3": {
        "font_size": typography.size.xl2,
        "font_weight": typography.weight.semibold,
        "line_height": typography.line_height.snug,
        "letter_spacing": typography.letter_spacing.normal,
    },
    "h4": {
        "font_size": typography.size.xl,
        "font_weight": typography.weight.semibold,
        "line_height": typography.line_height.snug,
        "letter_spacing": typography.letter_spacing.normal,
    },
    "h5": {
        "font_size": typography.size.lg,
        "font_weight": typography.weight.medium,
        "line_height": typography.line_height.normal,
        "letter_spacing": typography.letter_spacing.normal,
    },
    "h6": {
        "font_size": typography.size.base,
        "font_weight": typography.weight.medium,
        "line_height": typography.line_height.normal,
        "letter_spacing": typography.letter_spacing.normal,
    },
}

BODY_STYLES = {
    "body_lg": {
        "font_size": typography.size.lg,
        "font_weight": typography.weight.regular,
        "line_height": typography.line_height.relaxed,
    },
    "body": {
        "font_size": typography.size.base,
        "font_weight": typography.weight.regular,
        "line_height": typography.line_height.normal,
    },
    "body_sm": {
        "font_size": typography.size.sm,
        "font_weight": typography.weight.regular,
        "line_height": typography.line_height.normal,
    },
    "caption": {
        "font_size": typography.size.xs,
        "font_weight": typography.weight.regular,
        "line_height": typography.line_height.normal,
    },
}

BUTTON_STYLES = {
    "button_lg": {
        "font_size": typography.size.base,
        "font_weight": typography.weight.semibold,
        "line_height": typography.line_height.none,
        "letter_spacing": typography.letter_spacing.wide,
    },
    "button": {
        "font_size": typography.size.sm,
        "font_weight": typography.weight.semibold,
        "line_height": typography.line_height.none,
        "letter_spacing": typography.letter_spacing.wide,
    },
    "button_sm": {
        "font_size": typography.size.xs,
        "font_weight": typography.weight.semibold,
        "line_height": typography.line_height.none,
        "letter_spacing": typography.letter_spacing.wider,
    },
}
