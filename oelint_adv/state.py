from typing import List
from colorama import Fore
from colorama.ansi import AnsiCodes


class State():
    """State/Configuration shared between processes."""

    def __init__(self) -> None:
        self.color = False
        self.inline_suppressions = {}
        self.messageformat = ''
        self.no_info = False
        self.no_warn = False
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

    def get_colorize(self) -> bool:
        """Returns weather or not the terminal output is to be colorized"""
        return self.color

    def get_color_by_severity(self, severity: str) -> AnsiCodes:
        """Get an ANSI color code given a severity

        Args:
            severity (str): either `neutral`, `info`, `warning` or `error`
        """
        return self.__colors_by_severity.get(severity, '')

    def get_noinfo(self) -> bool:
        """--noinfo flag set

        Returns:
            bool: noinfo flag is set
        """
        return self.no_info

    def get_nowarn(self) -> bool:
        """--nowarn flag set

        Returns:
            bool: nowarn flag is set
        """
        return self.no_warn

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
