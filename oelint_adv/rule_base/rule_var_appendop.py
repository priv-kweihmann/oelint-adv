from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarAppendOperation(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.appendop",
                         severity="error",
                         message="Use '{}' instead of '{}' as it overwrites '{}'")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        _names = set([x.VarName for x in items if x.VarName != "inherit"])
        for name in _names:
            _weakest = [x for x in items if x.VarName == name and x.VarOp == " ??= "]
            _weak = [x for x in items if x.VarName == name and x.VarOp == " ?= "]
            _items = [x for x in items if x.VarName == name and x not in _weakest + _weak and x.VarOp in [" .= ", " += "]]
            for i in _items:
                if any(_weakest):
                    res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format('_append', i.VarOp, _weakest[0].Raw))
                elif any(x.Line > i.Line for x in _weak):
                    res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format('_append', i.VarOp, _weak[0].Raw))
            _items = [x for x in items if x.VarName == name and x not in _weakest + _weak and x.VarOp in [" =. ", " =+ "]]
            for i in _items:
                if any(_weakest):
                    res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format('_prepend', i.VarOp, _weakest[0].Raw))
                elif any(x.Line > i.Line for x in _weak):
                    res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format('_prepend', i.VarOp, _weak[0].Raw))
        return res
