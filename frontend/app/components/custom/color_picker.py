"""Color picker component."""

from typing import Any, Callable

from nicegui import ui

# Paleta de cores pré-definidas
PRESET_COLORS = [
    "#EF4444",  # Red
    "#F97316",  # Orange
    "#F59E0B",  # Amber
    "#EAB308",  # Yellow
    "#84CC16",  # Lime
    "#22C55E",  # Green
    "#10B981",  # Emerald
    "#14B8A6",  # Teal
    "#06B6D4",  # Cyan
    "#0EA5E9",  # Sky
    "#3B82F6",  # Blue
    "#6366F1",  # Indigo
    "#8B5CF6",  # Violet
    "#A855F7",  # Purple
    "#D946EF",  # Fuchsia
    "#EC4899",  # Pink
    "#F43F5E",  # Rose
    "#6B7280",  # Gray
]


class ColorPicker:
    """
    Componente de seleção de cor.

    Exibe paleta de cores pré-definidas + seletor customizado.

    Example:
        ```python
        picker = ColorPicker(label="Cor", value="#3B82F6")
        picker.on_change(lambda color: print(color))
        ```
    """

    def __init__(
        self,
        label: str,
        value: str = "#3B82F6",
        on_change: Callable[[str], None] | None = None,
        show_presets: bool = True,
    ) -> None:
        """
        Inicializa o ColorPicker.

        Args:
            label: Label do picker
            value: Cor inicial (hex)
            on_change: Callback ao mudar cor
            show_presets: Se True, mostra cores pré-definidas
        """
        self.label = label
        self._value = value
        self._on_change = on_change
        self.show_presets = show_presets

        # Container principal
        self.container = ui.column().classes("gap-2 w-full")

        with self.container:
            # Label
            ui.label(label).classes("text-sm font-medium")

            # Preview da cor atual
            with ui.row().classes("items-center gap-2"):
                self.preview = (
                    ui.element("div")
                    .classes("rounded")
                    .style(
                        f"width: 3rem; height: 3rem; background-color: {value}; "
                        "border: 2px solid #E5E7EB; cursor: pointer"
                    )
                )
                ui.label(value).classes("text-sm font-mono")

            # Input de cor nativo (oculto mas funcional)
            self.color_input = ui.color_input(value=value, on_change=self._handle_change)

            # Vincular clique no preview ao input
            self.preview.on("click", lambda: self.color_input.open())

            # Cores pré-definidas
            if show_presets:
                ui.label("Cores pré-definidas").classes("text-xs text-gray-500 mt-2")
                self._create_preset_grid()

    def _create_preset_grid(self) -> None:
        """Cria grid de cores pré-definidas."""
        with ui.grid(columns=9).classes("gap-2"):
            for color in PRESET_COLORS:
                self._create_color_swatch(color)

    def _create_color_swatch(self, color: str) -> None:
        """
        Cria quadrado de cor clicável.

        Args:
            color: Cor em hex
        """
        swatch = (
            ui.element("div")
            .classes("rounded cursor-pointer")
            .style(
                f"width: 2rem; height: 2rem; background-color: {color}; "
                "border: 2px solid #E5E7EB; transition: transform 0.2s"
            )
        )

        # Hover effect
        swatch.on("mouseenter", lambda: swatch.style("transform: scale(1.1)"))
        swatch.on("mouseleave", lambda: swatch.style("transform: scale(1)"))

        # Clicar seleciona a cor
        swatch.on("click", lambda: self._set_color(color))

    def _set_color(self, color: str) -> None:
        """
        Define nova cor.

        Args:
            color: Cor em hex
        """
        self._value = color
        self.preview.style(f"background-color: {color}")
        self.color_input.value = color

        if self._on_change:
            self._on_change(color)

    def _handle_change(self, e: Any) -> None:
        """Handler para mudança do input nativo."""
        self._set_color(self.color_input.value)

    @property
    def value(self) -> str:
        """Retorna cor atual."""
        return self._value

    @value.setter
    def value(self, color: str) -> None:
        """Define cor."""
        self._set_color(color)

    def on_change(self, callback: Callable[[str], None]) -> None:
        """Registra callback para mudanças."""
        self._on_change = callback


def create_color_picker(
    label: str,
    value: str = "#3B82F6",
    on_change: Callable[[str], None] | None = None,
    show_presets: bool = True,
) -> ColorPicker:
    """
    Função helper para criar ColorPicker.

    Args:
        label: Label do picker
        value: Cor inicial
        on_change: Callback ao mudar
        show_presets: Mostrar cores pré-definidas

    Returns:
        ColorPicker instance

    Example:
        >>> picker = create_color_picker("Cor da Categoria", value="#10B981")
    """
    return ColorPicker(
        label=label,
        value=value,
        on_change=on_change,
        show_presets=show_presets,
    )
