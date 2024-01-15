from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarDependsSingleLine(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.jetm.vars.dependssingleline',
                         severity='warning',
                         message='Each [R]DEPENDS entry should be put into a single line')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue=['DEPENDS', 'RDEPENDS'])
        for i in items:
            if len(i.get_items(versioned=True)) > 1:
                res += self.finding(i.Origin, i.InFileLine)
        return res
