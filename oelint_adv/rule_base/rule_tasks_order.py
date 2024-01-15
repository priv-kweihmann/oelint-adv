from typing import List, Tuple

from oelint_parser.cls_item import Function
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class TaskOrder(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.task.order',
                         severity='warning',
                         message='<FOO>',
                         appendix=CONSTANTS.FunctionsOrder)

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _files = {item.Origin for item in stash.GetItemsFor(
            filename=_file, classifier=Function.CLASSIFIER)}

        for _single_file in _files:
            items: List[Function] = stash.GetItemsFor(
                filename=_single_file, classifier=Function.CLASSIFIER, nolink=True)
            for item in items:
                _func_before = sorted(
                    [x for x in items if x.Line < item.Line and x.FuncName in CONSTANTS.FunctionsOrder], key=lambda x: x.Line, reverse=True)
                if any(_func_before):
                    _func_before = _func_before[0]
                    if item.FuncName not in CONSTANTS.FunctionsOrder:
                        continue
                    if CONSTANTS.FunctionsOrder.index(item.FuncName) < CONSTANTS.FunctionsOrder.index(_func_before.FuncName):
                        res += self.finding(item.Origin, item.InFileLine,
                                            '\'{a}\' should be placed before \'{b}\''.format(
                                                a=item.FuncName, b=_func_before.FuncName), appendix=item.FuncName)
        return res
