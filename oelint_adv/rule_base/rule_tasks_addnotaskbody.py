from oelint_adv.cls_item import Function
from oelint_adv.cls_item import TaskAdd
from oelint_adv.cls_rule import Rule
from oelint_adv.const_func import FUNC_ORDER


class TaskAddNoTaskBody(Rule):
    def __init__(self):
        super().__init__(id="oelint.task.addnotaskbody",
                         severity="warning",
                         message="The added task is not existing or has no body")

    def check(self, _file, stash):
        res = []
        for item in stash.GetItemsFor(filename=_file, classifier=TaskAdd.CLASSIFIER):
            if item.FuncName in FUNC_ORDER:
                # not for builtin types
                continue
            _ta = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER,
                                    attribute="FuncName", attributeValue=item.FuncName)
            if not any(_ta):
                res += self.finding(item.Origin, item.InFileLine)
            elif not any([x for x in _ta if x.FuncBodyStripped]):
                res += self.finding(item.Origin, item.InFileLine)
        return res
