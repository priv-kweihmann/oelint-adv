from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarSectionLowercase(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.doublemodify',
                         severity='error',
                         message='Multiple modifiers of append/prepend/remove/+= found in one operation')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if len(i.AppendOperation()) > 1:
                res += self.finding(i.Origin, i.InFileLine)
        return res
