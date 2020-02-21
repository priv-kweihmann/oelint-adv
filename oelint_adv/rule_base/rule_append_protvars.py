from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.const_vars import VAR_PROTECTED_APPEND


class VarQuoted(Rule):
    def __init__(self):
        super().__init__(id="oelint.append.protvars",
                         severity="error",
                         message="Variable '{VAR}' shouldn't be set as part of a bbappend",
                         onlyappend=True)

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in [x for x in items if x.VarName in VAR_PROTECTED_APPEND]:
            if i.VarOp not in [" ??= ", " ?= "]:
                res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.replace("{VAR}", i.VarName))
        return res
