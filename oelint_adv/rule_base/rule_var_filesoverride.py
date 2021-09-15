from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule

class VarFilesOverride(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.filesoverride",
                         severity="warning",
                         message="'{}' should not be overriden")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if i.VarName not in ["FILES"]:
                continue
            if not i.AppendOperation():
                res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format(i.VarName))
        return res
