from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.const_vars import get_protected_append_vars


class VarQuoted(Rule):
    def __init__(self):
        super().__init__(id="oelint.append.protvars",
                         severity="error",
                         message="Variable '{VAR}' shouldn't be set as part of a bbappend",
                         onlyappend=True,
                         appendix=get_protected_append_vars())

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in [x for x in items if x.VarName in get_protected_append_vars()]:
            if i.VarOp not in [" ??= ", " ?= "] and i.Flag not in ["vardeps", "vardepsexclude", "vardepvalue", "vardepvalueexclude"]:
                res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.replace("{VAR}", i.VarName), appendix=i.VarName)
        return res
