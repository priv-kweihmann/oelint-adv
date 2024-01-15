from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.parser import INLINE_BLOCK

from oelint_adv.cls_rule import Rule


class VarSRCUriSRCREVTag(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.srcurisrcrevtag',
                         severity='error',
                         message='\'tag\' in SRC_URI and a SRCREV for the same component doesn\'t compute')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')
        srcrevs: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                    attribute=Variable.ATTR_VAR, attributeValue='SRCREV')
        for item in items:
            lines = [y.strip('"') for y in item.get_items() if y and INLINE_BLOCK not in y]
            for x in lines:
                _url = stash.GetScrComponents(x)
                if _url['scheme'] in ['git'] and 'tag' in _url['options']:
                    if 'name' in _url['options']:
                        _srcrevs = [x for x in srcrevs if _url['options']['name'] in x.SubItems]
                    else:
                        _srcrevs = [x for x in srcrevs if not x.SubItems]
                    if any(_srcrevs):
                        res += self.finding(item.Origin, item.InFileLine)
        return res
