from typing import List, Tuple

from oelint_parser.cls_stash import Stash
from oelint_parser.cls_item import AddPylib

from oelint_adv.cls_rule import Rule, Classification


class AddpyLib(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.addpylib',
                         severity='error',
                         run_on=[Classification.BBCLASS, Classification.BBAPPEND, Classification.RECIPE],
                         message='addpylib is only valid in .conf files')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items_pylib: List[AddPylib] = stash.GetItemsFor(filename=_file, classifier=AddPylib.CLASSIFIER)
        for item in items_pylib:
            if not item.Origin.endswith('.conf'):  # pragma: no cover
                res += self.finding(item.Origin, item.InFileLine)
        return res
