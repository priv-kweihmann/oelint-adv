from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class LicenseSDPX(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.licensesdpx',
                         severity='warning',
                         message='LICENSE is not a valid OpenEmbedded SPDX expression')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='LICENSE')
        for i in items:
            if (('|' in i.VarValueStripped and ' | ' not in i.VarValueStripped) or
               ('&' in i.VarValueStripped and ' & ' not in i.VarValueStripped)):
                res += self.finding(i.Origin, i.InFileLine)
        return res
