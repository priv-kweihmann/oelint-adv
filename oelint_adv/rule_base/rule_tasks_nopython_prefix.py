import ast
import textwrap
from typing import List, Tuple

from oelint_parser.cls_item import Function
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class TaskNoPythonPrefix(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.task.nopythonprefix',
                         severity='warning',
                         message='Tasks that don\'t contain valid python code (e.g. shell code), should not be prefixed with python in function header')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Function] = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER)
        for item in items:
            try:
                ast.parse(textwrap.dedent(item.FuncBodyRaw.rstrip('}\n')), 'tempfile')
            except Exception:
                if item.IsPython:
                    res += self.finding(item.Origin, item.InFileLine)
        return res
