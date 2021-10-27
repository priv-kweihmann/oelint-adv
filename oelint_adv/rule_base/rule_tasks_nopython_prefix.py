import ast

from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Function


class TaskNoPythonPrefix(Rule):
    def __init__(self):
        super().__init__(id='oelint.task.nopythonprefix',
                         severity='warning',
                         message='Tasks containing shell code, should not be prefixed with python in function header')

    def check(self, _file, stash):
        res = []
        for item in stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER):
            try:
                ast.parse(item.FuncBodyRaw, 'tempfile')
            except Exception:
                if item.IsPython:
                    res += self.finding(item.Origin, item.InFileLine)
        return res
