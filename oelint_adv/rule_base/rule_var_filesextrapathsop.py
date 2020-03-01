from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarBugtrackerIsUrl(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.fileextrapathsop",
                         severity="error",
                         message="'FILESEXTRAPATHS' should only be used in combination with ' := '")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        for i in items:
            if i.VarName in ["FILESEXTRAPATHS_prepend", "FILESEXTRAPATHS_append", "FILESEXTRAPATHS"]:
                if i.VarOp != " := ":
                    res += self.finding(i.Origin, i.InFileLine)
        return res
