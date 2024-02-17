from typing import List, Tuple

from oelint_parser.cls_item import Function
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class TaskNoAnonPython(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.task.noanonpython',
                         severity='warning',
                         message='Avoid anonymous python functions as they expensive and come with all sorts of side effects')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Function.CLASSIFIER)
        for i in items:
            if i.IsPython and i.FuncName.strip() in ['', 'anonymous', '__anonymous']:
                res += self.finding(i.Origin, i.InFileLine)
        return res
