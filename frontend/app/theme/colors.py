"""Design System - Color Palette."""

from dataclasses import dataclass


@dataclass
class ColorPalette:
    """Paleta de cores do design system."""

    # Primary Colors (Azul)
    primary: str = "#3B82F6"  # blue-500
    primary_light: str = "#60A5FA"  # blue-400
    primary_dark: str = "#2563EB"  # blue-600

    # Secondary Colors (Roxo)
    secondary: str = "#8B5CF6"  # violet-500
    secondary_light: str = "#A78BFA"  # violet-400
    secondary_dark: str = "#7C3AED"  # violet-600

    # Success (Verde)
    success: str = "#10B981"  # green-500
    success_light: str = "#34D399"  # green-400
    success_dark: str = "#059669"  # green-600

    # Warning (Amarelo/Laranja)
    warning: str = "#F59E0B"  # amber-500
    warning_light: str = "#FBBF24"  # amber-400
    warning_dark: str = "#D97706"  # amber-600

    # Error (Vermelho)
    error: str = "#EF4444"  # red-500
    error_light: str = "#F87171"  # red-400
    error_dark: str = "#DC2626"  # red-600

    # Info (Ciano)
    info: str = "#06B6D4"  # cyan-500
    info_light: str = "#22D3EE"  # cyan-400
    info_dark: str = "#0891B2"  # cyan-600

    # Income (Verde claro)
    income: str = "#10B981"  # green-500
    income_bg: str = "#D1FAE5"  # green-100

    # Expense (Vermelho claro)
    expense: str = "#EF4444"  # red-500
    expense_bg: str = "#FEE2E2"  # red-100

    # Neutral Colors (Light Mode)
    bg_primary: str = "#FFFFFF"  # Fundo principal
    bg_secondary: str = "#F9FAFB"  # Fundo secundário (gray-50)
    bg_tertiary: str = "#F3F4F6"  # Fundo terciário (gray-100)

    text_primary: str = "#111827"  # Texto principal (gray-900)
    text_secondary: str = "#6B7280"  # Texto secundário (gray-500)
    text_tertiary: str = "#9CA3AF"  # Texto terciário (gray-400)

    border: str = "#E5E7EB"  # Bordas (gray-200)
    divider: str = "#E5E7EB"  # Divisores (gray-200)

    # Shadows
    shadow_sm: str = "0 1px 2px 0 rgb(0 0 0 / 0.05)"
    shadow_md: str = "0 4px 6px -1px rgb(0 0 0 / 0.1)"
    shadow_lg: str = "0 10px 15px -3px rgb(0 0 0 / 0.1)"


@dataclass
class DarkColorPalette(ColorPalette):
    """Paleta de cores para dark mode."""

    # Neutral Colors (Dark Mode)
    bg_primary: str = "#111827"  # Fundo principal (gray-900)
    bg_secondary: str = "#1F2937"  # Fundo secundário (gray-800)
    bg_tertiary: str = "#374151"  # Fundo terciário (gray-700)

    text_primary: str = "#F9FAFB"  # Texto principal (gray-50)
    text_secondary: str = "#D1D5DB"  # Texto secundário (gray-300)
    text_tertiary: str = "#9CA3AF"  # Texto terciário (gray-400)

    border: str = "#374151"  # Bordas (gray-700)
    divider: str = "#374151"  # Divisores (gray-700)

    # Backgrounds para income/expense (mais escuros no dark mode)
    income_bg: str = "#064E3B"  # green-900
    expense_bg: str = "#7F1D1D"  # red-900


# Instâncias globais
light_colors = ColorPalette()
dark_colors = DarkColorPalette()


def get_colors(dark_mode: bool = False) -> ColorPalette:
    """
    Retorna a paleta de cores apropriada.

    Args:
        dark_mode: Se True, retorna paleta dark

    Returns:
        Paleta de cores
    """
    return dark_colors if dark_mode else light_colors
