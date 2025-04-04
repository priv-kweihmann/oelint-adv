import os
from typing import List, Tuple

from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule, Classification


class FileNoSpaces(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.file.underscores',
                         severity='error',
                         message='FOO',
                         run_on=[Classification.RECIPE])

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _basename, _ext = os.path.splitext(os.path.basename(_file))
        if _ext in ['.bb']:  # pragma: no cover
            if stash.IsPackageGroup(_file) or stash.IsImage(_file):
                return []
            _us = [x for x in _basename if x == '_']
            if len(_us) > 1:
                res += self.finding(_file, 1,
                                    override_msg='Filename should not contain more than one \'_\'')
            elif not _us:
                res += self.finding(
                    _file, 1, override_msg='Filename should contain at least one \'_\' in the end')
        return res
