"""Input components."""

from typing import Any, Callable, Literal

from nicegui import ui

InputType = Literal["text", "number", "email", "password", "textarea"]


def create_input(
    label: str,
    value: str = "",
    placeholder: str = "",
    input_type: InputType = "text",
    on_change: Callable | None = None,
    required: bool = False,
    disabled: bool = False,
    validation: dict[str, Any] | None = None,
) -> ui.input:
    """
    Cria input customizado.

    Args:
        label: Label do input
        value: Valor inicial
        placeholder: Placeholder
        input_type: Tipo do input
        on_change: Callback ao mudar valor
        required: Se True, campo obrigatório
        disabled: Se True, campo desabilitado
        validation: Dicionário de validações Quasar

    Returns:
        ui.input instance

    Example:
        >>> create_input("Nome", placeholder="Digite seu nome", required=True)
    """
    input_elem = ui.input(
        label=label,
        value=value,
        placeholder=placeholder,
        on_change=on_change,
    )

    # Aplicar tipo
    if input_type == "number":
        input_elem.props('type="number"')
    elif input_type == "email":
        input_elem.props('type="email"')
    elif input_type == "password":
        input_elem.props('type="password"')
    elif input_type == "textarea":
        input_elem = ui.textarea(
            label=label,
            value=value,
            placeholder=placeholder,
            on_change=on_change,
        )

    # Aplicar classes
    input_elem.classes("w-full")

    # Required
    if required:
        input_elem.props("required")

    # Disabled
    if disabled:
        input_elem.props("disable")

    # Validações
    if validation:
        rules = []
        if validation.get("min_length"):
            rules.append(
                f"val => val.length >= {validation['min_length']} || 'Mínimo {validation['min_length']} caracteres'"
            )
        if validation.get("max_length"):
            rules.append(
                f"val => val.length <= {validation['max_length']} || 'Máximo {validation['max_length']} caracteres'"
            )
        if validation.get("pattern"):
            rules.append(f"val => /{validation['pattern']}/.test(val) || 'Formato inválido'")

        if rules:
            input_elem.props(f':rules="[{", ".join(rules)}]"')

    return input_elem


def create_select(
    label: str,
    options: list[str] | dict[str, str],
    value: str | None = None,
    on_change: Callable | None = None,
    required: bool = False,
    disabled: bool = False,
    clearable: bool = True,
) -> ui.select:
    """
    Cria select customizado.

    Args:
        label: Label do select
        options: Lista de opções ou dict {value: label}
        value: Valor inicial
        on_change: Callback ao mudar
        required: Campo obrigatório
        disabled: Campo desabilitado
        clearable: Permite limpar seleção

    Returns:
        ui.select instance

    Example:
        >>> create_select("Tipo", options={"income": "Receita", "expense": "Despesa"})
    """
    select = ui.select(
        label=label,
        options=options,
        value=value,
        on_change=on_change,
    )

    select.classes("w-full")

    if required:
        select.props("required")

    if disabled:
        select.props("disable")

    if clearable:
        select.props("clearable")

    return select


def create_date_input(
    label: str,
    value: str = "",
    on_change: Callable | None = None,
    required: bool = False,
    disabled: bool = False,
    min_date: str | None = None,
    max_date: str | None = None,
) -> ui.input:
    """
    Cria input de data.

    Args:
        label: Label do input
        value: Valor inicial (formato: YYYY-MM-DD)
        on_change: Callback ao mudar
        required: Campo obrigatório
        disabled: Campo desabilitado
        min_date: Data mínima (YYYY-MM-DD)
        max_date: Data máxima (YYYY-MM-DD)

    Returns:
        ui.input instance

    Example:
        >>> create_date_input("Data", value="2025-10-13")
    """
    date_input = ui.input(
        label=label,
        value=value,
        on_change=on_change,
    )

    date_input.props('type="date"')
    date_input.classes("w-full")

    if required:
        date_input.props("required")

    if disabled:
        date_input.props("disable")

    if min_date:
        date_input.props(f'min="{min_date}"')

    if max_date:
        date_input.props(f'max="{max_date}"')

    # Adicionar ícone de calendário
    with date_input:
        ui.icon("event").classes("cursor-pointer")

    return date_input


def create_number_input(
    label: str,
    value: float | int = 0,
    on_change: Callable | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
    step: float = 1,
    required: bool = False,
    disabled: bool = False,
    prefix: str | None = None,
    suffix: str | None = None,
) -> ui.number:
    """
    Cria input numérico.

    Args:
        label: Label do input
        value: Valor inicial
        on_change: Callback ao mudar
        min_value: Valor mínimo
        max_value: Valor máximo
        step: Incremento
        required: Campo obrigatório
        disabled: Campo desabilitado
        prefix: Prefixo (ex: "R$")
        suffix: Sufixo (ex: "%")

    Returns:
        ui.number instance

    Example:
        >>> create_number_input("Valor", prefix="R$", min_value=0, step=0.01)
    """
    number_input = ui.number(
        label=label,
        value=value,
        on_change=on_change,
    )

    number_input.classes("w-full")

    if min_value is not None:
        number_input.props(f'min="{min_value}"')

    if max_value is not None:
        number_input.props(f'max="{max_value}"')

    number_input.props(f'step="{step}"')

    if required:
        number_input.props("required")

    if disabled:
        number_input.props("disable")

    if prefix:
        number_input.props(f'prefix="{prefix}"')

    if suffix:
        number_input.props(f'suffix="{suffix}"')

    return number_input
