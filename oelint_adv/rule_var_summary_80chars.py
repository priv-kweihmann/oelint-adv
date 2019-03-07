try:
    from .cls_rule import Rule
    from .cls_item import *
except (SystemError, ImportError):
    from cls_rule import Rule
    from cls_item import *

class VarSummary80Chars(Rule):
    def __init__(self):
        super().__init__(id = "oelint.vars.summary80chars", 
                         severity="warning",
                         message="'SUMMARY' should not be longer than 80 characters")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue="SUMMARY")
        for i in items:
            val = i.VarValue.strip()
            if len(val) > 80:
                res += self.finding(i.Origin, i.InFileLine)
        return res