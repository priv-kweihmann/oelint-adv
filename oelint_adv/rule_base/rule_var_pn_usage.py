from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarPnBpnUsage(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.pnbpnusage',
                         severity='error',
                         message='${BPN} should be used instead of ${PN}')

    def __getMatches(self, _file: str, stash: Stash) -> List[Variable]:
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')
        for i in items:
            for x in i.get_items():
                _comp = stash.GetScrComponents(x)
                if '${PN}' in _comp['src']:
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
            i.RealRaw = i.RealRaw.replace('${PN}', '${BPN}')
            i.Raw = i.Raw.replace('${PN}', '${BPN}')
            res.append(_file)
        return res
