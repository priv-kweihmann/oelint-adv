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
        summary = ''.join(stash.ExpandVar(_file, attribute=Variable.ATTR_VAR, attributeValue='SUMMARY').get('SUMMARY', ['']))
        desc = ''.join(stash.ExpandVar(_file, attribute=Variable.ATTR_VAR,
                       attributeValue='DESCRIPTION').get('DESCRIPTION', ['']))
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='DESCRIPTION')
        if len(desc.strip()) < len(summary.strip()) and items:
            res += self.finding(items[0].Origin, items[0].InFileLine)
        return res
