from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarAppendOperation(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.appendop",
                         severity="warning",
                         message="Use '_append' instead of ' += '")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if i.VarName == "inherit":
                continue
            if " += " in i.AppendOperation():
                res += self.finding(i.Origin, i.InFileLine)
        return res
