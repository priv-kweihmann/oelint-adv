from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class VarSectionLowercase(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.notneededspace',
                         severity='info',
                         message='Space at the beginning of the var is not needed')

    def __getMatches(self, _file: str, stash: Stash) -> List[Variable]:
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in [x for x in items if 'append' not in x.SubItems]:
            if i.VarValueStripped.startswith(' '):
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
            i.RealRaw = RegexRpl.sub(r'"\s+', '"', i.RealRaw) + '\n'
            i.Raw = RegexRpl.sub(r'"\s+', '"', i.Raw) + '\n'
            i.VarValue = RegexRpl.sub(r'"\s+', '"', i.VarValue) + '\n'
            res.append(_file)
        return res
