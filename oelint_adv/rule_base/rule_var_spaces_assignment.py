from typing import List, Tuple

from oelint_parser.cls_item import FlagAssignment, Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarSpacesOnAssignment(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.spacesassignment',
                         severity='warning',
                         message='Suggest spaces around assignment. E.g. \'FOO = "BAR"\'')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=[Variable.CLASSIFIER, FlagAssignment.CLASSIFIER])
        for i in items:
            if i.VarOp not in Variable.VAR_VALID_OPERATOR:
                res += self.finding(i.Origin, i.InFileLine)
        return res
