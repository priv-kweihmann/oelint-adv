from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarsDownloadfilename(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.downloadfilename',
                         severity='warning',
                         message='Fetcher does create a download artifact without \'PV\' in the filename')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')

        _pv = stash.ExpandTerm(_file, '${PV}')

        for i in items:
            for item in [stash.ExpandTerm(_file, x) for x in i.get_items()]:
                _scrcomp = stash.GetScrComponents(item)
                if _scrcomp.get('scheme', '') in ['https', 'http', 'ftp']:
                    _src = _scrcomp.get('src', '')
                    _dfn = _scrcomp.get('options', {}).get(
                        'downloadfilename', '')

                    if _pv not in _src:
                        if _dfn and _pv in _dfn:
                            continue
                        res += self.finding(i.Origin, i.InFileLine)
        return res
