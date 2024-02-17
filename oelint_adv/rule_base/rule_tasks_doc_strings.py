from typing import List, Tuple

from oelint_parser.cls_item import FlagAssignment, Function
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class TaskDocStrings(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.task.docstrings',
                         severity='info',
                         message='Every custom task should have a doc string set by task[doc] = \'\'')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for item in stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER):
            if item.FuncName in CONSTANTS.FunctionsKnown or item.FuncName in ['', 'anonymous', '__anonymous']:
                # Skip for builtin tasks or anonymous python functions
                continue
            if item.IsAppend():
                # In case it's an append operation, there has to be an original
                # so don't raise any warnings here
                continue
            _ta: List[FlagAssignment] = stash.GetItemsFor(filename=_file,
                                                          classifier=FlagAssignment.CLASSIFIER,
                                                          attribute=FlagAssignment.ATTR_NAME,
                                                          attributeValue=item.FuncName)
            if not any(x.Flag == 'doc' for x in _ta):
                res += self.finding(item.Origin, item.InFileLine)
        return res
