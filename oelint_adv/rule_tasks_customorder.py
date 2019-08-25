from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import *
from oelint_adv.const_func import FUNC_ORDER
import os


class TaskCustomOrder(Rule):
    def __init__(self):
        super().__init__(id="oelint.task.customorder",
                         severity="error",
                         message="<FOO>")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=TaskAdd.CLASSIFIER)
        for item in items:
            _before = item.Before
            _after = item.After
            for _a in _after:
                if not _a in FUNC_ORDER:
                    continue
                _ai = FUNC_ORDER.index(_a)
                for _b in _before:
                    if not _b in FUNC_ORDER:
                        continue
                    _bi = FUNC_ORDER.index(_b)
                    if _ai > _bi:
                        self.OverrideMsg(
                            "after '{}' and before '{}' breaks ordering cylce".format(_a, _b))
                        res += self.finding(item.Origin, item.InFileLine)
        return res
