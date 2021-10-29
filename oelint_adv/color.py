from colorama import Fore
from colorama.ansi import AnsiCodes

_COLOR = False
_COLORS_BY_SEVERITY = {
    'info': Fore.GREEN,
    'warning': Fore.YELLOW,
    'error': Fore.RED,
}


def get_colorize() -> bool:
    """Returns weather or not the terminal output is to be colorized"""
    return _COLOR


def set_colorize(value: bool) -> None:
    """Globally turn colored terminal output on/off"""
    global _COLOR
    _COLOR = value


def get_color_by_severity(severity: str) -> AnsiCodes:
    """Get an ANSI color code given a severity

    Args:
        severity (str): either `neutral`, `info`, `warning` or `error`
    """
    return _COLORS_BY_SEVERITY.get(severity, '')
