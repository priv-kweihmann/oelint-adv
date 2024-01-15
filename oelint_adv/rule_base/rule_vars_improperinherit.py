from typing import List, Tuple

from oelint_parser.cls_item import Inherit
from oelint_parser.cls_stash import Stash
from oelint_parser.parser import INLINE_BLOCK
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class VarImproperInherit(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.improperinherit',
                         severity='error',
                         message='\'{inherit}\' is not a proper bbclass name')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Inherit.CLASSIFIER)
        for i in items:
            for subi in [stash.ExpandTerm(_file, x) for x in i.get_items() if x and x != INLINE_BLOCK]:
                if not RegexRpl.match(r'^[A-Za-z0-9_.-]+$', subi):
                    res += self.finding(i.Origin, i.InFileLine,
                                        self.Msg.replace('{inherit}', subi))
        return res
