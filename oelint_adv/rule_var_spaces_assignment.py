try:
    from .cls_rule import Rule
    from .cls_item import *
except (SystemError, ImportError):
    from cls_rule import Rule
    from cls_item import *

class VarSpacesOnAssignment(Rule):
    def __init__(self):
        super().__init__(id = "oelint.vars.spacesassignment", 
                         severity="warning",
                         message="Suggest spaces around variable assignment. E.g. 'FOO = \"BAR\"'")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if i.VarName == "inherit":
                continue
            needle = " = "
            if i.IsAppend():
                needle = " += "
            if i.Raw.find(needle) == -1:
                res += self.finding(i.Origin, i.InFileLine)
        return res