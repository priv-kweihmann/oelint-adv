from typing import List, Tuple

from oelint_parser.cls_item import Include, Inherit, Item, Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarDependsAppend(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.dependsappend',
                         severity='error',
                         message='DEPENDS should only be appended, not overwritten after an include or inherit')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='DEPENDS')
        incinh: List[Item] = stash.GetItemsFor(filename=_file, classifier=[
                                               Inherit.CLASSIFIER, Include.CLASSIFIER], nolink=True)

        earliest = 99999999
        if incinh:
            earliest = min(x.Line for x in incinh)

        for i in items:
            if not i.AppendOperation() and i.Line > earliest:
                res += self.finding(i.Origin, i.InFileLine)
        return res
