from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.const_vars import get_protected_vars


class VarQuoted(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.bbvars",
                         severity="warning",
                         message="Variable '{VAR}' should be set on a disto/layer or local.conf level, not in a recipe",
                         appendix=get_protected_vars())

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in [x for x in items if x.VarName in get_protected_vars()]:
            if i.VarOp not in [" ??= ", " ?= "]:
                res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.replace("{VAR}", i.VarName), appendix=i.VarName)
        return res
