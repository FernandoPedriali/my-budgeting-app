"""Currency input component."""

from decimal import Decimal
from typing import Any, Callable

from nicegui import ui


class CurrencyInput:
    """
    Input formatado para moeda brasileira (BRL).

    Formata automaticamente o valor conforme o usuário digita.

    Example:
        ```python
        currency = CurrencyInput(label="Valor", value=1234.56)
        currency.on_change(lambda v: print(f"Valor: {v}"))
        ```
    """

    def __init__(
        self,
        label: str,
        value: Decimal | float = Decimal("0.00"),
        placeholder: str = "R$ 0,00",
        on_change: Callable[[Decimal], None] | None = None,
        required: bool = False,
        disabled: bool = False,
        allow_negative: bool = False,
    ) -> None:
        """
        Inicializa o CurrencyInput.

        Args:
            label: Label do input
            value: Valor inicial
            placeholder: Placeholder
            on_change: Callback ao mudar valor
            required: Campo obrigatório
            disabled: Campo desabilitado
            allow_negative: Permite valores negativos
        """
        self.label = label
        self._value = Decimal(str(value))
        self.placeholder = placeholder
        self._on_change = on_change
        self.required = required
        self.disabled = disabled
        self.allow_negative = allow_negative

        # Criar input
        self.input = ui.input(
            label=label,
            placeholder=placeholder,
            value=self._format_display(self._value),
        )

        self.input.classes("w-full")
        self.input.props('prefix="R$"')

        if required:
            self.input.props("required")

        if disabled:
            self.input.props("disable")

        # Vincular eventos
        self.input.on("blur", self._on_blur)
        self.input.on("focus", self._on_focus)

    def _format_display(self, value: Decimal) -> str:
        """
        Formata valor para exibição.

        Args:
            value: Valor decimal

        Returns:
            String formatada (ex: "1.234,56")
        """
        formatted = f"{float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted

    def _parse_input(self, text: str) -> Decimal:
        """
        Parse string para Decimal.

        Args:
            text: Texto do input

        Returns:
            Valor decimal
        """
        # Remover caracteres não numéricos (exceto - e ,)
        cleaned = ""
        for char in text:
            if char.isdigit() or char in ",-":
                cleaned += char

        # Substituir vírgula por ponto
        cleaned = cleaned.replace(".", "").replace(",", ".")

        # Converter para Decimal
        try:
            value = Decimal(cleaned)
            if not self.allow_negative and value < 0:
                value = Decimal("0.00")
            return value
        except:
            return Decimal("0.00")

    def _on_blur(self, e: Any) -> None:
        """Formata ao perder foco."""
        text = self.input.value or "0"
        value = self._parse_input(text)
        self._value = value
        self.input.value = self._format_display(value)

        if self._on_change:
            self._on_change(value)

    def _on_focus(self, e: Any) -> None:
        """Remove formatação ao ganhar foco (facilita edição)."""
        # Mantém formatação mas seleciona tudo
        pass

    @property
    def value(self) -> Decimal:
        """Retorna o valor atual como Decimal."""
        return self._value

    @value.setter
    def value(self, new_value: Decimal | float) -> None:
        """Define novo valor."""
        self._value = Decimal(str(new_value))
        self.input.value = self._format_display(self._value)

    def on_change(self, callback: Callable[[Decimal], None]) -> None:
        """
        Registra callback para mudanças de valor.

        Args:
            callback: Função a ser chamada com o novo valor
        """
        self._on_change = callback


def create_currency_input(
    label: str,
    value: Decimal | float = Decimal("0.00"),
    on_change: Callable[[Decimal], None] | None = None,
    required: bool = False,
    disabled: bool = False,
    allow_negative: bool = False,
) -> CurrencyInput:
    """
    Função helper para criar CurrencyInput.

    Args:
        label: Label do input
        value: Valor inicial
        on_change: Callback ao mudar
        required: Campo obrigatório
        disabled: Campo desabilitado
        allow_negative: Permite negativos (para estornos)

    Returns:
        CurrencyInput instance

    Example:
        >>> currency = create_currency_input(
        ...     "Valor",
        ...     value=1500.00,
        ...     on_change=lambda v: print(v)
        ... )
    """
    return CurrencyInput(
        label=label,
        value=value,
        on_change=on_change,
        required=required,
        disabled=disabled,
        allow_negative=allow_negative,
    )
