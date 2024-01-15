from typing import List, Tuple

from oelint_parser.cls_item import Item
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class NoSpaceEmptyLineRule(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.spaces.emptyline',
                         severity='warning',
                         message='Empty lines shall not contain spaces')

    def __getMatches(self, _file: str, stash: Stash) -> List[Item]:
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw.strip('\n') and not i.Raw.strip():
                res.append(i)  # pragma: no cover
        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for i in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, i.InFileLine)  # pragma: no cover
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:  # pragma: no cover
        res = []
        for i in self.__getMatches(_file, stash):
            i.RealRaw = '\n'
            i.Raw = '\n'
            res.append(_file)
        return res
