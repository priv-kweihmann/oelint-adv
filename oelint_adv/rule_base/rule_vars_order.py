from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.const_vars import VAR_ORDER


class VarsOrder(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.order",
                         severity="warning",
                         message="<FOO>",
                         appendix=[self.__cleanname(x) for x in VAR_ORDER])

    def __cleanname(self, _input):
        return _input.replace("$", "").replace("{", "").replace("}", "")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for item in items:
            _func_before = sorted(
                [x for x in items if x.Line < item.Line and x.VarName in VAR_ORDER], key=lambda x: x.Line, reverse=True)
            if any(_func_before):
                _func_before = _func_before[0]
                if item.VarName not in VAR_ORDER:
                    continue
                if VAR_ORDER.index(item.VarName) < VAR_ORDER.index(_func_before.VarName):
                    res += self.finding(item.Origin, item.InFileLine,
                                        "'{}' should be placed before '{}'".format(
                                            item.VarName, _func_before.VarName), appendix=self.__cleanname(item.VarName))
        return res
