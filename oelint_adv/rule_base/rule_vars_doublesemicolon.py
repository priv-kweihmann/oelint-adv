from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class VarsDoubleSemicolon(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.doublesemicolon',
                         severity='info',
                         message='";;" is not needed')

    def __getMatches(self, _file: str, stash: Stash) -> List[Variable]:
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue=CONSTANTS.GetByPath('oelint-semicolon-vars'))
        for i in items:
            if ';;' in i.VarValue:
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
            i.RealRaw = RegexRpl.sub(r';{2,}', ';', i.RealRaw)
            i.Raw = RegexRpl.sub(r';{2,}', ';', i.Raw)
            i.VarValue = RegexRpl.sub(r';{2,}', ';', i.VarValue)
            res.append(_file)
        return res
