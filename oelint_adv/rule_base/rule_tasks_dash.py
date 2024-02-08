from typing import List, Tuple

from oelint_parser.cls_item import Function, PythonBlock, TaskAdd, TaskDel
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class TaskDash(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.task.dash',
                         severity='error',
                         message='Task \'{FUNC}\' shall not have \'-\' in its name')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for item in stash.GetItemsFor(filename=_file, classifier=(
                TaskAdd.CLASSIFIER, Function.CLASSIFIER,
                PythonBlock.CLASSIFIER, TaskDel.CLASSIFIER)):
            value = item.FuncName
            if '-' in value:
                res += self.finding(item.Origin, item.InFileLine,
                                    self.Msg.replace('{FUNC}', value))
        return res
