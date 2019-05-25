try:
    from .cls_rule import Rule
    from .cls_item import *
    from .const_func import FUNC_ORDER
except (SystemError, ImportError):
    from cls_rule import Rule
    from cls_item import *
    from const_func import FUNC_ORDER
import os

class TaskMultiAppends(Rule):
    def __init__(self):
        super().__init__(id = "oelint.task.multiappends", 
                         severity="error",
                         message="Multiple appends to the same function in the same file won't work in bitbake")

    def check(self, _file, stash):
        res = []
        _stash = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER)
        for item in _stash:
            if not item.SubItem:
                continue
            if len([x for x in _stash if x.FuncName == item.FuncName and x.SubItem == item.SubItem and not x.IsFromAppend()]) > 1:
                res += self.finding(item.Origin, item.InFileLine)
        return res