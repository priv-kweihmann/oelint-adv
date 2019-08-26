from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import *
import os


class VarOverride(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.override",
                         severity="error",
                         message="<FOO>")

    def check(self, _file, stash):
        res = []
        __varnames = [x.VarName for x in stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)]
        for v in __varnames:
            if v == "inherit":
                # This will be done by another rule
                continue
            items = stash.GetItemsFor(
                filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue=v)
            items = sorted(items, key=lambda x: x.Line, reverse=False)
            if len(items) > 1:
                if all([not x.IsAppend() for x in items]):
                    self.OverrideMsg("Variable '{}' is set by {}".format(
                        v, ",".join([os.path.basename(x.Origin) for x in items])))
                    res += self.finding(items[0].Origin, items[0].InFileLine)
        return res
