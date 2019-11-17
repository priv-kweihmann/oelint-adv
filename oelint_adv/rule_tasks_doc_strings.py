from oelint_adv.cls_item import Function
from oelint_adv.cls_item import TaskAssignment
from oelint_adv.cls_rule import Rule
from oelint_adv.const_func import FUNC_ORDER


class TaskDocStrings(Rule):
    def __init__(self):
        super().__init__(id="oelint.task.docstrings",
                         severity="info",
                         message="Every custom task should have a doc string set by task[doc] = \"\"")

    def check(self, _file, stash):
        res = []
        for item in stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER):
            if item.FuncName in FUNC_ORDER:
                # Skip for buildin tasks
                continue
            _ta = stash.GetItemsFor(filename=_file, classifier=TaskAssignment.CLASSIFIER,
                                    attribute="FuncName", attributeValue=item.FuncName)
            if not any(_ta):
                res += self.finding(item.Origin, item.InFileLine)
        return res
