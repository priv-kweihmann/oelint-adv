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
        _map = {}
        for i in items:
            for incname in RegexRpl.split(r'\s|,', i.IncName):
                if not incname or not incname.strip():
                    continue  # pragma: no cover
                key = i.FileIncluded if i.FileIncluded else incname.strip()
                if key not in _map:
                    _map[key] = {'key': incname.strip(), 'value': 0, 'origin': i}
                _map[key]['value'] += 1
        for _, value in _map.items():
            if value.get('value', 0) > 1:
                res += self.finding(value.get('origin').Origin,
                                    value.get('origin').InFileLine,
                                    self.Msg.replace('{INC}', value.get('key')))
        return res
