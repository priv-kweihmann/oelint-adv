from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.const_vars import SUGGESTED_VARS


class VarSuggestedExists(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.suggestedvar",
                         severity="info",
                         message="<FOO>")

    def check(self, _file, stash):
        res = []
        for var in SUGGESTED_VARS:
            items = stash.GetItemsFor(
                filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue=var)
            if not any(items):
                res += self.finding(_file, 0, "Variable '{}' should be set".format(var))
        return res
