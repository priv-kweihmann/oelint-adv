from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarBbclassextend(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.bbclassextend",
                         severity="info",
                         message="BBCLASSEXTEND should be set if possible")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="BBCLASSEXTEND")
        items_inherit = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue="inherit")
        if not any(items):
            if not any([x for x in items_inherit if x.VarValue.find("native") != -1]):
                res += self.finding(_file, 0)
        return res
