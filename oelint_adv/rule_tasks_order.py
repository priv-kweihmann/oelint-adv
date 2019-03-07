try:
    from .cls_rule import Rule
    from .cls_item import *
    from .const_func import FUNC_ORDER
except (SystemError, ImportError):
    from cls_rule import Rule
    from cls_item import *
    from const_func import FUNC_ORDER
import os

class TaskOrder(Rule):
    def __init__(self):
        super().__init__(id = "oelint.task.order", 
                         severity="warning",
                         message="<FOO>")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER)
        for item in items:
            _func_before = sorted([x for x in items if x.Line < item.Line and x.FuncName in FUNC_ORDER], key=lambda x: x.Line, reverse=True)
            if any(_func_before):
                _func_before = _func_before[0]
                if not item.FuncName in FUNC_ORDER:
                    continue
                if FUNC_ORDER.index(item.FuncName) < FUNC_ORDER.index(_func_before.FuncName):
                    self.OverrideMsg("'{}' should be placed before '{}'".format(item.FuncName, _func_before.FuncName))
                    res += self.finding(item.Origin, item.InFileLine)
        return res