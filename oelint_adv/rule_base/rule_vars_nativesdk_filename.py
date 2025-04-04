from typing import List, Tuple

from oelint_parser.cls_item import Inherit
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule, Classification


class VarNativeSDKFilename(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.nativesdkfilename',
                         severity='warning',
                         run_on=[Classification.BBAPPEND, Classification.RECIPE],
                         message='nativesdk-recipe-files should include \'nativesdk-\' in file name')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Inherit] = [x for x in
                                stash.GetItemsFor(filename=_file, classifier=Inherit.CLASSIFIER)
                                if 'nativesdk' in x.get_items()]
        if any(items):
            if _file.find('nativesdk-') == -1:
                res += self.finding(_file, 0)
        return res
