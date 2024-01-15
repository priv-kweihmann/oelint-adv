from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarAutorev(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.autorev',
                         severity='warning',
                         message='The usage of \'AUTOREV\' for SRCREV leads to not reproducible builds')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR)
        for i in [x for x in items if x.VarName.startswith('SRCREV')]:
            if i.VarValueStripped == '${AUTOREV}':
                res += self.finding(i.Origin, i.InFileLine)
        return res
