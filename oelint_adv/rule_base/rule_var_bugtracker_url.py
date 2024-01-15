from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarBugtrackerIsUrl(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.bugtrackerisurl',
                         severity='warning',
                         message='\'BUGTRACKER\' should be an URL')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='BUGTRACKER')
        for i in items:
            val_ = i.VarValueStripped
            try:
                result = stash.GetScrComponents(val_)
                if not result['scheme'] or not result['src']:
                    raise Exception()
            except Exception:
                res += self.finding(i.Origin, i.InFileLine)
        return res
