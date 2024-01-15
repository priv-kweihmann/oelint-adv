from typing import List, Tuple

from oelint_parser.cls_item import Include
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class FileReqIncNoRelPaths(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.file.includerelpath',
                         severity='warning',
                         message='include or require statements should not use relative paths. Try using bbclasses instead')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for item in stash.GetItemsFor(filename=_file,
                                      classifier=Include.CLASSIFIER):
            _path = stash.ExpandTerm(_file, item.IncName)
            if '..' in _path.split('/'):
                res += self.finding(item.Origin, item.InFileLine)
        return res
