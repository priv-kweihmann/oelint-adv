from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.const_vars import get_suggested_vars


class VarSuggestedExists(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.suggestedvar",
                         severity="info",
                         message="<FOO>",
                         onappend=False,
                         appendix=get_suggested_vars())

    def check(self, _file, stash):
        res = []
        _is_pkg_group = False
        for i in stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER, 
                                   attribute=Variable.ATTR_VAR, attributeValue="inherit"):
            if any(x == "packagegroup" for x in i.get_items()):
                _is_pkg_group = True
                break
        for var in get_suggested_vars():
            if _is_pkg_group and var in ["LICENSE", "CVE_PRODUCT"]:
                continue
            items = stash.GetItemsFor(
                filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue=var)
            if not any(items):
                res += self.finding(_file, 0, "Variable '{}' should be set".format(var), appendix=var)
        return res
