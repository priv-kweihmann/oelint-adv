import os
from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarBugtrackerIsUrl(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.fileextrapaths',
                         severity='warning',
                         message='\'FILESEXTRAPATHS\' shouldn\'t be used in a bb file')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='FILESEXTRAPATHS')
        for i in items:
            _, ext = os.path.splitext(i.Origin)
            if ext == '.bb':
                res += self.finding(i.Origin, i.InFileLine)
        return res
