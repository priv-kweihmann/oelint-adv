from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarTrailingSlash(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.notrailingslash',
                         severity='error',
                         message='\'{a}\' must not end with a \'/\'')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue=['S', 'B', 'T', 'D'])
        for i in items:
            _expanded = stash.ExpandTerm(_file, i.VarValueStripped)
            if _expanded.endswith('/'):
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(a=i.VarName))
        return res
