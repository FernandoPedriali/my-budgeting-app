"""Formatting utilities."""

from datetime import date, datetime
from decimal import Decimal


def format_currency(value: Decimal | float, show_symbol: bool = True) -> str:
    """
    Formata valor como moeda brasileira.

    Args:
        value: Valor a formatar
        show_symbol: Se True, mostra símbolo R$

    Returns:
        String formatada (ex: "R$ 1.234,56")

    Examples:
        >>> format_currency(1234.56)
        'R$ 1.234,56'
        >>> format_currency(1234.56, show_symbol=False)
        '1.234,56'
    """
    if isinstance(value, Decimal):
        value = float(value)

    # Formatar com separadores brasileiros
    formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    if show_symbol:
        return f"R$ {formatted}"
    return formatted


def format_date(value: date | datetime, format: str = "dd/MM/yyyy") -> str:
    """
    Formata data no padrão brasileiro.

    Args:
        value: Data a formatar
        format: Formato desejado

    Returns:
        String formatada

    Examples:
        >>> format_date(date(2025, 10, 13))
        '13/10/2025'
    """
    if isinstance(value, datetime):
        value = value.date()

    if format == "dd/MM/yyyy":
        return value.strftime("%d/%m/%Y")
    elif format == "dd/MM/yy":
        return value.strftime("%d/%m/%y")
    elif format == "dd MMM yyyy":
        months = {
            1: "Jan",
            2: "Fev",
            3: "Mar",
            4: "Abr",
            5: "Mai",
            6: "Jun",
            7: "Jul",
            8: "Ago",
            9: "Set",
            10: "Out",
            11: "Nov",
            12: "Dez",
        }
        return f"{value.day:02d} {months[value.month]} {value.year}"
    else:
        return value.strftime(format)


def format_datetime(value: datetime, format: str = "dd/MM/yyyy HH:mm") -> str:
    """
    Formata data e hora.

    Args:
        value: DateTime a formatar
        format: Formato desejado

    Returns:
        String formatada

    Examples:
        >>> format_datetime(datetime(2025, 10, 13, 14, 30))
        '13/10/2025 14:30'
    """
    if format == "dd/MM/yyyy HH:mm":
        return value.strftime("%d/%m/%Y %H:%M")
    elif format == "dd/MM/yyyy HH:mm:ss":
        return value.strftime("%d/%m/%Y %H:%M:%S")
    else:
        return value.strftime(format)


def format_number(value: int | float, decimals: int = 0) -> str:
    """
    Formata número com separadores brasileiros.

    Args:
        value: Número a formatar
        decimals: Casas decimais

    Returns:
        String formatada

    Examples:
        >>> format_number(1234567)
        '1.234.567'
        >>> format_number(1234.567, decimals=2)
        '1.234,57'
    """
    if decimals == 0:
        return f"{int(value):,}".replace(",", ".")
    else:
        formatted = f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Formata valor como percentual.

    Args:
        value: Valor a formatar (0.5 = 50%)
        decimals: Casas decimais

    Returns:
        String formatada

    Examples:
        >>> format_percentage(0.5)
        '50,0%'
        >>> format_percentage(0.1234, decimals=2)
        '12,34%'
    """
    percentage = value * 100
    formatted = f"{percentage:.{decimals}f}".replace(".", ",")
    return f"{formatted}%"


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Trunca texto longo.

    Args:
        text: Texto a truncar
        max_length: Tamanho máximo
        suffix: Sufixo a adicionar

    Returns:
        Texto truncado

    Examples:
        >>> truncate_text("Texto muito longo aqui", max_length=10)
        'Texto m...'
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def format_relative_date(value: date) -> str:
    """
    Formata data relativa (hoje, ontem, etc).

    Args:
        value: Data a formatar

    Returns:
        String formatada

    Examples:
        >>> format_relative_date(date.today())
        'Hoje'
    """
    today = date.today()
    delta = (today - value).days

    if delta == 0:
        return "Hoje"
    elif delta == 1:
        return "Ontem"
    elif delta == -1:
        return "Amanhã"
    elif 2 <= delta <= 7:
        return f"Há {delta} dias"
    elif -7 <= delta <= -2:
        return f"Em {abs(delta)} dias"
    else:
        return format_date(value)
