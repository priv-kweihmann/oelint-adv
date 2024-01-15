from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.parser import INLINE_BLOCK

from oelint_adv.cls_rule import Rule


class VarSRCURIWildcard(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.srcuriwildcard',
                         severity='error',
                         message='\'SRC_URI\' should not contain any wildcards')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                   attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')
        for item in _items:
            for f in [x.strip('\'') for x in item.get_items() if x and INLINE_BLOCK not in x]:
                components = stash.GetScrComponents(f)
                if components['scheme'] == 'file':
                    if any(x for x in ['*'] if x in components['src']):
                        res += self.finding(item.Origin, item.InFileLine)
        return res
