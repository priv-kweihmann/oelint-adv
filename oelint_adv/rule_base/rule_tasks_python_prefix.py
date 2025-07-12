import ast
import textwrap
from typing import List, Tuple

from oelint_parser.cls_item import Function
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class TaskPythonPrefix(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.task.pythonprefix',
                         severity='warning',
                         message='Tasks containing python code, should be prefixed with python in function header')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Function] = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER)
        for item in items:
            # Don't make assumptions about functions that consist of single
            # line only
            if len([x for x in item.FuncBodyRaw.split('\n') if x.strip()]) < 2:
                continue
            try:
                ast.parse(textwrap.dedent(item.FuncBodyRaw.rstrip('}\n')), 'tempfile')
                if not item.IsPython:
                    res += self.finding(item.Origin, item.InFileLine)
            except Exception as e:  # noqa: S110
                print(e)
                pass  # noqa: S110 - intentionally ignore all errors
        return res
