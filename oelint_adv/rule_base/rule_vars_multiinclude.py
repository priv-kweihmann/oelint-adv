from typing import List, Tuple

from oelint_parser.cls_item import Include
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class VarMultiInclude(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.multiinclude',
                         severity='warning',
                         message='\'{INC}\' is included multiple times')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Include] = stash.GetItemsFor(filename=_file, classifier=Include.CLASSIFIER)
        keys = []
        for i in items:
            keys += [x.strip() for x in RegexRpl.split(r'\s|,', i.IncName) if x]
        for key in list(set(keys)):
            _i = [x for x in items if x.IncName.find(key) != -1]
            if len(_i) > 1:
                res += self.finding(_i[-1].Origin, _i[-1].InFileLine, self.Msg.replace('{INC}', key))
        return res
