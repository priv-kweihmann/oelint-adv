from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import *
import re


class VarMultiInherit(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.multiinherit",
                         severity="warning",
                         message="'{INH}' is included multiple times")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="inherit")
        keys = []
        for i in items:
            keys += [x.strip() for x in re.split("\s|,", i.VarValue) if x]
        for key in list(set(keys)):
            _i = [x for x in items if x.VarValue.find(key) != -1]
            if len(_i) > 1:
                res += self.finding(_i[-1].Origin, _i[-1].InFileLine,
                                    self.Msg.replace("{INH}", key))
        return res
