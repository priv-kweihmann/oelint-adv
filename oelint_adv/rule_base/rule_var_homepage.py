from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarHomepagePrefix(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.homepageprefix',
                         severity='warning',
                         message='\'HOMEPAGE\' should start with \'http://\' or \'https://\'')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='HOMEPAGE')
        for i in items:
            if not any(x for x in ['https://', 'http://'] if i.VarValueStripped.strip().startswith(x)):
                res += self.finding(i.Origin, i.InFileLine)
        return res
