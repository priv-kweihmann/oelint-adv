from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.helper_files import get_scr_components
from oelint_adv.parser import INLINE_BLOCK
import re


class VarSRCURIWildcard(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.srcuriwildcard",
                         severity="error",
                         message="'SRC_URI' should not contain any wildcards")

    def check(self, _file, stash):
        res = []
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
        for i in _items:
            for f in [x.strip('"') for x in i.get_items() if x]:
                if f == INLINE_BLOCK:
                    continue
                components = get_scr_components(f)
                if components["scheme"] == "file":
                    if any([x for x in ["*"] if x in components["src"]]):
                        res += self.finding(i.Origin, i.InFileLine)
        return res
