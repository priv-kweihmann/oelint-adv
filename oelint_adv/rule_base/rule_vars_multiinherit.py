from typing import List, Tuple

from oelint_parser.cls_item import Inherit
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarMultiInherit(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.multiinherit',
                         severity='warning',
                         message='\'{inherit}\' is included multiple times')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Inherit] = stash.GetItemsFor(filename=_file, classifier=Inherit.CLASSIFIER)
        keys = []
        for i in items:
            for y in i.get_items():
                if y not in keys:
                    keys.append(y)
                else:
                    res += self.finding(i.Origin, i.InFileLine,
                                        self.Msg.replace('{inherit}', y))
        return res
