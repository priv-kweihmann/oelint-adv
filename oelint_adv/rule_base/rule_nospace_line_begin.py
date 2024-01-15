from typing import List, Tuple

from oelint_parser.cls_item import Function, Item, PythonBlock
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class NoSpaceBeginningRule(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.spaces.linebeginning',
                         severity='warning',
                         message='Line shall not begin with a space')

    def __getMatches(self, _file: str, stash: Stash) -> List[Item]:
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw and i.Raw.startswith(' '):
                res.append(i)
        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for i in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, i.InFileLine)
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        for i in self.__getMatches(_file, stash):
            if isinstance(i, PythonBlock) or isinstance(i, Function):
                continue  # pragma: no cover
            i.RealRaw = i.RealRaw.lstrip(' ')
            i.Raw = i.Raw.lstrip(' ')
            res.append(_file)
        return res
