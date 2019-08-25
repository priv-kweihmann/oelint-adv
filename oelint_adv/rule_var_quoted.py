from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import *


class VarQuoted(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.valuequoted",
                         severity="error",
                         message="Variable value should be quoted")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if i.VarName == "inherit":
                continue
            val = i.VarValue.strip()
            if not val.startswith("\"") or not val.endswith("\""):
                res += self.finding(i.Origin, i.InFileLine)
        return res
