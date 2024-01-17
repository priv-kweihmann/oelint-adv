from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarDescSame(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.descriptionsame',
                         severity='warning',
                         message='\'DESCRIPTION\' is the same a \'SUMMARY\' - it can be removed then')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='DESCRIPTION')
        items_sum: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                      attribute=Variable.ATTR_VAR, attributeValue='SUMMARY')
        for i in items:
            _same = [x for x in items_sum if x.VarValueStripped == i.VarValueStripped]
            if any(_same):
                res += self.finding(i.Origin, i.InFileLine)
        return res
