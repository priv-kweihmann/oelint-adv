try:
    from .cls_rule import Rule
    from .cls_item import *
except (SystemError, ImportError):
    from cls_rule import Rule
    from cls_item import *

class VarSectionLowercase(Rule):
    def __init__(self):
        super().__init__(id = "oelint.vars.sectionlowercase", 
                         severity="warning",
                         message="'SECTION' should only lowercase characters")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue="SECTION")
        for i in items:
            if not i.VarValue.islower():
                res += self.finding(i.Origin, i.InFileLine)
        return res