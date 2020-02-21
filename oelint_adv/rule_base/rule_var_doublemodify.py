from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarSectionLowercase(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.doublemodify",
                         severity="error",
                         message="Multiple modifiers of append/prepend/remove/+= found in one operation")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in [x for x in items]:
            if len(i.AppendOperation()) > 1:
                res += self.finding(i.Origin, i.InFileLine)
        return res
