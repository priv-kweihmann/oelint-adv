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
        summary = ''.join(stash.ExpandVar(_file, attribute=Variable.ATTR_VAR, attributeValue='SUMMARY').get('SUMMARY', ['']))
        desc = ''.join(stash.ExpandVar(_file, attribute=Variable.ATTR_VAR,
                       attributeValue='DESCRIPTION').get('DESCRIPTION', ['']))
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='DESCRIPTION')
        if desc.strip() == summary.strip() and items:
            res += self.finding(items[0].Origin, items[0].InFileLine)
        return res
