from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarAppendOperation(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.appendop",
                         severity="error",
                         message="Use '_append' instead of ' += '")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        _names = set([x.VarName for x in items if x.VarName != "inherit"])
        for name in _names:
            _items = [x for x in items if x.VarName == name]
            if len(_items) > 1:
                _operations = set([x.VarOp for x in _items])
                if " += " in _operations and any(x in _operations for x in [" ??= "]):
                    for i in [x for x in _items if " += " in x.AppendOperation()]:
                        res += self.finding(i.Origin, i.InFileLine)
        return res
