from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.parser import INLINE_BLOCK

from oelint_adv.cls_rule import Rule


class VarSRCUriOptions(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.srcuridomains',
                         severity='warning',
                         message='Recipe is pulling from different domains, this will likely cause issues')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')

        _domains = {'default': set()}
        _override_ignores = ['append', 'remove', 'prepend']
        for item in items:
            _overrides = '-'.join(sorted([x for x in item.SubItems if x not in _override_ignores])) or 'default'
            _is_append = item.IsAppend()
            _is_remove = 'remove' in item.AppendOperation()
            if _overrides not in _domains:
                _domains[_overrides] = set()
            for u in [x.strip('\'').strip() for x in item.get_items()]:
                if u == INLINE_BLOCK:
                    continue
                _url = stash.GetScrComponents(u)
                if _url['scheme'] and _url['scheme'] not in ['file']:
                    domain = _url['src'].split('/')[0]
                    if _is_append:
                        _domains[_overrides].add(domain)
                    elif _is_remove and domain in _domains[_overrides]:
                        _domains[_overrides].remove(domain)
                    else:
                        _domains[_overrides] = {domain}
        for _, v in _domains.items():
            if len(v) > 1:
                res += self.finding(item.Origin, item.InFileLine)
        return res
