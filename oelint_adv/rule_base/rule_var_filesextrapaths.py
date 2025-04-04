from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule, Classification


class VarBugtrackerIsUrl(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.fileextrapaths',
                         severity='warning',
                         run_on=[Classification.BBCLASS, Classification.DISTROCONF,
                                 Classification.LAYERCONF, Classification.MACHINECONF, Classification.RECIPE],
                         message='\'FILESEXTRAPATHS\' should be used only in a bbappend file')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='FILESEXTRAPATHS')
        for i in items:
            if not i.Origin.endswith('.bbappend'):  # pragma: no cover
                res += self.finding(i.Origin, i.InFileLine)
        return res
