import re

from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.parser import INLINE_BLOCK
from oelint_adv.helper_files import expand_term


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
            for subi in [expand_term(stash, _file, x) for x in i.get_items() if x and x != INLINE_BLOCK]:
                if not re.match(r"^[A-Za-z0-9_.-]+$", subi):
                    res += self.finding(i.Origin, i.InFileLine,
                                        self.Msg.replace("{INH}", subi))
        return res
