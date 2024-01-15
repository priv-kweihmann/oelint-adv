from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarQuoted(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.valuequoted',
                         severity='error',
                         message='Variable value should be quoted')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            # Don't use VarValueStripped here as we explicitly want the quotes
            # at the beginning and the end of the value
            val_ = i.VarValue.strip()
            if ((not val_.startswith('"') or not val_.endswith('"'))
                    and (not val_.startswith('\'') or not val_.endswith('\''))):  # noqa: W503
                res += self.finding(i.Origin, i.InFileLine)
        return res
