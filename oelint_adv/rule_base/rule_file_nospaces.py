from typing import List, Tuple

from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class FileNoSpaces(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.file.nospaces',
                         severity='error',
                         message='Path to file contains spaces. Please remove them')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _layer_root = stash.GetLayerRoot(_file)
        _relpath = _file.replace(_layer_root, '').lstrip('/')
        if ' ' in _relpath:
            res += self.finding(_file, 1)
        return res
