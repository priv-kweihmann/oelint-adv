import os
from typing import List, Tuple

from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class BBClassUnderscore(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.bbclass.underscores',
                         severity='error',
                         message='bbclass filenames should not contain \'_\'. Replace it by \'-\'')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _files = {x.Origin for x in stash.GetItemsFor(filename=_file) if x.Origin.endswith('.bbclass')}
        for file in _files:
            if '_' in os.path.basename(file):
                res += self.finding(file, 1)
        return res
