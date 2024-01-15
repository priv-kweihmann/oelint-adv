from typing import List, Tuple

from oelint_parser.cls_item import Item
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class NoTabs(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.tabs.notabs',
                         severity='warning',
                         message='Don\'t use tabs use spaces')

    def __getMatches(self, _file: str, stash: Stash) -> List[Item]:
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw and '\t' in i.Raw:
                res.append(i)
        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for i in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, i.InFileLine)
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:  # pragma: no cover
        res = []  # pragma: no cover
        for i in self.__getMatches(_file, stash):  # pragma: no cover
            i.RealRaw = RegexRpl.sub(r'\t', '    ', i.RealRaw)  # pragma: no cover
            i.Raw = RegexRpl.sub(r'\t', '    ', i.Raw)  # pragma: no cover
            res.append(_file)  # pragma: no cover
        return res  # pragma: no cover
