from oelint_adv.cls_item import Function
from oelint_adv.cls_rule import Rule
from oelint_adv.const_func import FUNC_ORDER


class TaskOrder(Rule):
    def __init__(self):
        super().__init__(id="oelint.task.order",
                         severity="warning",
                         message="<FOO>",
                         appendix=FUNC_ORDER)

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Function.CLASSIFIER)
        for item in items:
            _func_before = sorted(
                [x for x in items if x.Line < item.Line and x.FuncName in FUNC_ORDER], key=lambda x: x.Line, reverse=True)
            if any(_func_before):
                _func_before = _func_before[0]
                if item.FuncName not in FUNC_ORDER:
                    continue
                if FUNC_ORDER.index(item.FuncName) < FUNC_ORDER.index(_func_before.FuncName):
                    res += self.finding(item.Origin, item.InFileLine,
                                        "'{}' should be placed before '{}'".format(
                                            item.FuncName, _func_before.FuncName), appendix=item.FuncName)
        return res
