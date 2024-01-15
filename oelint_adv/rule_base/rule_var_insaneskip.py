from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarInsaneSkip(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.insaneskip',
                         severity='error',
                         message='INSANE_SKIP should be avoided at any cost')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='INSANE_SKIP')
        for i in items:
            res += self.finding(i.Origin, i.InFileLine)
        return res
