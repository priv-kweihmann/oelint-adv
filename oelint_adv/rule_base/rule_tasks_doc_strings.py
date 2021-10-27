from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Function
from oelint_parser.cls_item import TaskAssignment
from oelint_parser.constants import CONSTANTS


class TaskDocStrings(Rule):
    def __init__(self):
        super().__init__(id='oelint.task.docstrings',
                         severity='info',
                         message='Every custom task should have a doc string set by task[doc] = \'\'')

    def check(self, _file, stash):
        res = []
        for item in stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER):
            if item.FuncName in CONSTANTS.FunctionsKnown or not item.FuncName:
                # Skip for buildin tasks or anonymous python functions
                continue
            if item.IsAppend():
                # In case it's an append operation, there has to be an original
                # so don't raise any warnings here
                continue
            _ta = stash.GetItemsFor(filename=_file, classifier=TaskAssignment.CLASSIFIER,
                                    attribute='FuncName', attributeValue=item.FuncName)
            if not any(_ta):
                res += self.finding(item.Origin, item.InFileLine)
        return res
