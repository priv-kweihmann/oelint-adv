from typing import List, Tuple

from oelint_parser.cls_item import Include
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class FileIncludeVsRequire(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.file.requireinclude',
                         severity='warning',
                         message='Use \'require {FILE}\' instead of \'include {FILE}\'')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for item in stash.GetItemsFor(filename=_file,
                                      classifier=Include.CLASSIFIER):
            if item.Statement == 'include':
                res += self.finding(item.Origin, item.InFileLine,
                                    self.Msg.replace('{FILE}', item.IncName))
        return res
