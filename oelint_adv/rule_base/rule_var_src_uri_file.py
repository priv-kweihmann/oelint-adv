from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.parser import INLINE_BLOCK

from oelint_adv.cls_rule import Rule


class VarSRCUriFirstFile(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.srcurifile',
                         severity='warning',
                         message='First item of SRC_URI should not be a file:// fetcher, if multiple fetcher are used')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')
        _fetcher = []
        for item in items:
            lines = [y.strip('"') for y in item.get_items() if y]

            for x in lines:
                if x == INLINE_BLOCK:
                    _fetcher.append(('inline', item.InFileLine))
                    continue
                _url = stash.GetScrComponents(x)
                if _url['scheme']:
                    _fetcher.append((_url['scheme'], item.InFileLine))
        if _fetcher:
            if any(x[0] not in ['file', 'inline'] for x in _fetcher) and _fetcher[0][0] == 'file':
                res += self.finding(item.Origin, _fetcher[0][1])
        return res
