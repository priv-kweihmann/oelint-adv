from typing import List, Tuple

from oelint_parser.cls_item import Function
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class TaskInstallNoMkdir(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.task.nomkdir',
                         severity='error',
                         message='\'mkdir\' shall not be used in do_install. Use \'install\'')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Function] = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER)
        for item in items:
            if item.FuncName.startswith('do_install'):
                if item.FuncBody.find(' mkdir ') != -1:
                    res += self.finding(item.Origin, item.InFileLine)
        return res
