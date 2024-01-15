from typing import List, Tuple

from oelint_parser.cls_item import Inherit, Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarBbclassextend(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.bbclassextend',
                         severity='info',
                         message='BBCLASSEXTEND should be set if possible')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='BBCLASSEXTEND')
        items_inherit: List[Inherit] = stash.GetItemsFor(filename=_file, classifier=Inherit.CLASSIFIER)
        if not any(items):
            _safe = False
            for item in items_inherit:
                if any(x in ['native', 'nativesdk', 'cross'] for x in item.get_items()):
                    _safe = True
                    break
            if not _file.endswith('.bbappend') and not _safe:
                res += self.finding(_file, 0)
        return res
