from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarSummary80Chars(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.summary80chars',
                         severity='warning',
                         message='\'SUMMARY\' should not be longer than 80 characters')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='SUMMARY')
        for i in items:
            if len(i.VarValueStripped) > 80:
                res += self.finding(i.Origin, i.InFileLine)
        return res
