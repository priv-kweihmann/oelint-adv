from typing import List, Tuple

from oelint_parser.cls_item import Inherit
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarNativeFilename(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.nativefilename',
                         severity='warning',
                         message='native-recipe-files should include \'-native\' in file name')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Inherit] = [x for x in stash.GetItemsFor(
            filename=_file, classifier=Inherit.CLASSIFIER) if 'native' in x.get_items()]
        if any(items):
            if _file.find('-native') == -1:
                res += self.finding(_file, 0)
        return res
