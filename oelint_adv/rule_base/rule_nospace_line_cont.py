from typing import List, Tuple

from oelint_parser.cls_item import Comment, Item
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class NoSpaceRuleCont(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.spaces.linecont',
                         severity='error',
                         message='No spaces after line continuation')

    def __getMatches(self, _file: str, stash: Stash) -> List[Item]:
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if isinstance(i, Comment):
                continue
            if i.Raw:  # pragma: no cover
                if RegexRpl.search(r'\\\s+\n', i.Raw):
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
            i.RealRaw = RegexRpl.sub(r'\\\s+\n', '\\\n', i.RealRaw)
            i.Raw = RegexRpl.sub(r'\\\s+\n', '\\\n', i.Raw)
            res.append(_file)
        return res
