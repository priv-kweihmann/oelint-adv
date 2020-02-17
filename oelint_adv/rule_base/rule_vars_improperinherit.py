import re

from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.helper_files import safe_linesplit


class VarImproperInherit(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.improperinherit",
                         severity="error",
                         message="'{INH}' is not a proper bbclass name")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="inherit")
        for i in items:
            for subi in [x for x in safe_linesplit(i.VarValueStripped) if x]:
                if not re.match(r"^[A-Za-z0-9_.-]+$", subi):
                    res += self.finding(i.Origin, i.InFileLine,
                                        self.Msg.replace("{INH}", subi))
        return res
