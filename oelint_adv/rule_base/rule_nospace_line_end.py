from typing import List, Tuple

from oelint_parser.cls_item import Item
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class NoSpaceTrailingRule(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.spaces.lineend',
                         severity='warning',
                         message='Line shall not end with a space')

    def __getMatches(self, _file: str, stash: Stash) -> List[Tuple[Item, int]]:
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            _linecnt = 0
            for line in i.Raw.split('\n'):
                if line.endswith(' '):
                    res.append((i, i.InFileLine + _linecnt, i.InFileLine))
                _linecnt += 1
        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for (i, line, blockoffset) in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, line, blockoffset=blockoffset)
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        for i in self.__getMatches(_file, stash):
            i[0].RealRaw = RegexRpl.sub(r'\s+\n', '\n', i[0].RealRaw)
            i[0].Raw = RegexRpl.sub(r'\s+\n', '\n', i[0].Raw)
            res.append(_file)
        return res
