from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarPnUsageDiscouraged(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.pnusagediscouraged',
                         severity='warning',
                         message='Variable shouldn\'t contain ${PN} or ${BPN}')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        needles = ['SUMMARY', 'HOMEPAGE', 'BUGTRACKER', 'DESCRIPTION']
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue=needles)
        for i in items:
            if '${PN}' in i.VarValue or '${BPN}' in i.VarValue:
                res += self.finding(i.Origin, i.InFileLine)
        return res
