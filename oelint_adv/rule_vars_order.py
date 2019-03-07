try:
    from .cls_rule import Rule
    from .cls_item import *
    from .const_vars import VAR_ORDER
except (SystemError, ImportError):
    from cls_rule import Rule
    from cls_item import *
    from const_vars import VAR_ORDER
import os

class VarsOrder(Rule):
    def __init__(self):
        super().__init__(id = "oelint.var.order", 
                         severity="warning",
                         message="<FOO>")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for item in items:
            _func_before = sorted([x for x in items if x.Line < item.Line and x.VarName in VAR_ORDER], key=lambda x: x.Line, reverse=True)
            if any(_func_before):
                _func_before = _func_before[0]
                if not item.VarName in VAR_ORDER:
                    continue
                if VAR_ORDER.index(item.VarName) < VAR_ORDER.index(_func_before.VarName):
                    self.OverrideMsg("'{}' should be placed before '{}'".format(item.VarName, _func_before.VarName))
                    res += self.finding(item.Origin, item.InFileLine)
        return res