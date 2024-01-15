from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarSectionLowercase(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.sectionlowercase',
                         severity='warning',
                         message='\'SECTION\' should only lowercase characters')

    def __getMatches(self, _file: str, stash: Stash) -> List[Variable]:
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='SECTION')
        for i in items:
            if not i.VarValue.islower():
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
            i.RealRaw = i.RealRaw.replace(i.VarValue, i.VarValue.lower())
            i.Raw = i.Raw.replace(i.VarValue, i.VarValue.lower())
            i.VarValue = i.VarValue.lower()
            res.append(_file)
        return res
