"""Design System - Spacing & Sizing."""

from dataclasses import dataclass


@dataclass
class Spacing:
    """Sistema de espaçamento (baseado em 4px)."""

    px: str = "1px"
    xs: str = "0.25rem"  # 4px
    sm: str = "0.5rem"  # 8px
    md: str = "1rem"  # 16px
    lg: str = "1.5rem"  # 24px
    xl: str = "2rem"  # 32px
    xl2: str = "2.5rem"  # 40px
    xl3: str = "3rem"  # 48px
    xl4: str = "4rem"  # 64px
    xl5: str = "6rem"  # 96px
    xl6: str = "8rem"  # 128px


@dataclass
class BorderRadius:
    """Raios de borda."""

    none: str = "0"
    sm: str = "0.25rem"  # 4px
    md: str = "0.375rem"  # 6px
    lg: str = "0.5rem"  # 8px
    xl: str = "0.75rem"  # 12px
    xl2: str = "1rem"  # 16px
    xl3: str = "1.5rem"  # 24px
    full: str = "9999px"  # Totalmente arredondado


@dataclass
class Size:
    """Tamanhos fixos."""

    # Ícones
    icon_xs: str = "1rem"  # 16px
    icon_sm: str = "1.25rem"  # 20px
    icon_md: str = "1.5rem"  # 24px
    icon_lg: str = "2rem"  # 32px
    icon_xl: str = "2.5rem"  # 40px

    # Avatares
    avatar_xs: str = "1.5rem"  # 24px
    avatar_sm: str = "2rem"  # 32px
    avatar_md: str = "2.5rem"  # 40px
    avatar_lg: str = "3rem"  # 48px
    avatar_xl: str = "4rem"  # 64px

    # Botões (altura)
    button_sm: str = "2rem"  # 32px
    button_md: str = "2.5rem"  # 40px
    button_lg: str = "3rem"  # 48px

    # Inputs (altura)
    input_sm: str = "2rem"  # 32px
    input_md: str = "2.5rem"  # 40px
    input_lg: str = "3rem"  # 48px

    # Sidebar
    sidebar_width: str = "16rem"  # 256px
    sidebar_collapsed_width: str = "4rem"  # 64px

    # Container
    container_sm: str = "640px"
    container_md: str = "768px"
    container_lg: str = "1024px"
    container_xl: str = "1280px"
    container_2xl: str = "1536px"


@dataclass
class ZIndex:
    """Níveis de empilhamento."""

    dropdown: int = 1000
    sticky: int = 1020
    fixed: int = 1030
    modal_backdrop: int = 1040
    modal: int = 1050
    popover: int = 1060
    tooltip: int = 1070


@dataclass
class Breakpoint:
    """Breakpoints responsivos."""

    sm: str = "640px"
    md: str = "768px"
    lg: str = "1024px"
    xl: str = "1280px"
    xl2: str = "1536px"


# Instâncias globais
spacing = Spacing()
border_radius = BorderRadius()
size = Size()
z_index = ZIndex()
breakpoint = Breakpoint()


# Grid System (baseado em 12 colunas)
GRID_COLUMNS = 12
GRID_GAP = spacing.md  # 16px


# Component Spacing Presets
COMPONENT_SPACING = {
    "card_padding": spacing.lg,  # 24px
    "card_gap": spacing.md,  # 16px
    "modal_padding": spacing.xl,  # 32px
    "form_field_gap": spacing.md,  # 16px
    "button_padding_x": spacing.lg,  # 24px
    "button_padding_y": spacing.sm,  # 8px
    "input_padding_x": spacing.md,  # 16px
    "input_padding_y": spacing.sm,  # 8px
    "section_gap": spacing.xl2,  # 40px
    "page_padding": spacing.xl,  # 32px
}
