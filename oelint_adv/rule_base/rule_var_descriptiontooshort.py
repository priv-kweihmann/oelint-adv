from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarDescSameTooBrief(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.descriptiontoobrief',
                         severity='warning',
                         message='\'DESCRIPTION\' is the shorter than \'SUMMARY\'')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='DESCRIPTION')
        items_sum: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                      attribute=Variable.ATTR_VAR, attributeValue='SUMMARY')
        for i in items:
            _same = [x for x in items_sum if len(x.VarValueStripped) > len(i.VarValueStripped)]
            if any(_same):
                res += self.finding(i.Origin, i.InFileLine)
        return res
