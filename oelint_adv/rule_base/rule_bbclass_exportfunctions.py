from typing import List, Tuple

from oelint_parser.cls_item import FunctionExports
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule, Classification


class ExportFunctionsDash(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.exportfunction.dash',
                         severity='error',
                         run_on=[Classification.BBCLASS],
                         message='EXPORT_FUNCTIONS should not contain \'-\', replace by \'_\'.')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for item in stash.GetItemsFor(filename=_file,
                                      classifier=FunctionExports.CLASSIFIER):
            if any('-' in x for x in item.get_items()):
                res += self.finding(_file, item.InFileLine)
        return res
