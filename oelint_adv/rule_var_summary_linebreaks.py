try:
    from .cls_rule import Rule
    from cls_rule import Rule
except (SystemError, ImportError):
    from cls_rule import Rule
    from cls_item import *

class VarSummaryLinebreaks(Rule):
    def __init__(self):
        super().__init__(id = "oelint.vars.summarylinebreaks", 
                         severity="warning",
                         message="'SUMMARY' should not contain line breaks")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue="SUMMARY")
        for i in items:
            if i.Raw.strip().find("\\n") != -1:
                res += self.finding(i.Origin, i.InFileLine)
        return res