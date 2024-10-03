from typing import List
from colorama import Fore
from colorama.ansi import AnsiCodes

from oelint_adv.caches import Caches


class State():
    """State/Configuration shared between processes."""

    def __init__(self) -> None:
        self.color = False
        self.inline_suppressions = {}
        self.messageformat = ''
        self.hide = {'error': False, 'warning': False, 'info': False, 'inactive': True}
        self.rel_path = False
        self.rule_file = {}
        self.suppression = []
        self.nobackup = False
        self.additional_stash_args = {}

        self.__colors_by_severity = {
            'info': Fore.GREEN,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
        }

        self._seen_inline_suppressions = []
        self._caches: Caches = None

    def get_colorize(self) -> bool:
        """Returns weather or not the terminal output is to be colorized"""
        return self.color

    def get_color_by_severity(self, severity: str) -> AnsiCodes:
        """Get an ANSI color code given a severity

        Args:
            severity (str): either `neutral`, `info`, `warning` or `error`
        """
        return self.__colors_by_severity.get(severity, '')

    def get_hide(self, severity) -> bool:
        """--hide severity is set

        Returns:
            bool: hide messages of given severity
        """
        return self.hide.get(severity, True)

    def get_relpaths(self) -> bool:
        """--relpath flag is set

        Returns:
            bool: relpath is set
        """
        return self.rel_path

    def get_messageformat(self) -> str:
        """Get messageformat

        Returns:
            str: message format
        """
        return self.messageformat

    def get_suppressions(self) -> List[str]:
        """Get suppressions

        Returns:
            List[str]: Set suppressions
        """
        return self.suppression

    def get_rulefile(self) -> dict:
        """Rule file

        Returns:
            dict: set rule file
        """
        return self.rule_file

    def get_inlinesuppressions(self) -> dict:
        """Inline suppressions

        Returns:
            dict: Set inline suppressions
        """
        return self.inline_suppressions

    def get_nobackup(self) -> bool:
        """nobackup set

        Returns:
            bool: nobackup is set
        """
        return self.nobackup  # pragma: no cover

    def get_additional_stash_args(self) -> dict:
        """Additional arguments for the Stash init

        Returns:
            dict: additional args
        """
        return self.additional_stash_args

    def set_inline_suppression_seen(self, file: str, line: int, ids: List[str]) -> None:
        """Announce that inline suppression have been used

        Args:
            file (str): File path
            line (int): Line
            ids (List[str]): IDs of suppression
        """
        self._seen_inline_suppressions += [(file, line, x) for x in ids]

    def get_inline_suppression_seen(self, file: str, line: int, id_: str) -> bool:
        """Check if inline suppression have been used

        Args:
            file (str): File path
            line (int): Line
            id_ (str): ID of suppression

        Returns:
            bool: True if found
        """
        return (file, line, id_) in self._seen_inline_suppressions
