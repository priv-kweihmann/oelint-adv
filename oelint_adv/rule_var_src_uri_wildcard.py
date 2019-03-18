try:
    from .cls_rule import Rule
    from .cls_item import *
    from .helper_files import get_scr_components
except (SystemError, ImportError):
    from cls_rule import Rule
    from cls_item import *
    from helper_files import get_scr_components
from urllib.parse import urlparse
import os

class VarSRCURIWildcard(Rule):
    def __init__(self):
        super().__init__(id = "oelint.var.srcuriwildcard", 
                         severity="error",
                         message="'SRC_URI' should not contain any wildcards")

    def check(self, _file, stash):
        res = []
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
        for i in _items:
            for f in [x for x in i.VarValue.split(" ") if x]:
                components = get_scr_components(f)
                if components["proto"] == "file":
                    if any([x for x in ["*", "?"] if x in components["name"]]):
                        res += self.finding(i.Origin, i.InFileLine)
        return res