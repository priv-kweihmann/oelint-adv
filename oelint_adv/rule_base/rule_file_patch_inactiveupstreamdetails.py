import os
from typing import List, Tuple

import regex  # noqa: I900
from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule, Classification


class FilePatchIsUpstreamStatusInactiveUpstreamDetails(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.file.inactiveupstreamdetails',
                         severity='info',
                         run_on=[Classification.BBAPPEND, Classification.RECIPE],
                         message='Patch \'{FILE}\' with Upstream-Status: Inactive-Upstream has to have a lastcommit and/or lastrelease appended in []')

    def _get_recipe(self, items, path):
        # Find matching SRC_URI assignment
        return [x for x in items if x.VarValue.find(os.path.basename(path)) != -1]

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        patches = stash.GetFiles(_file, '*.patch')
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')

        _valid_class = {
            'Inactive-Upstream': r'Inactive-Upstream\s+\[\s*(lastcommit.+|lastrelease.+)+\s*\]',
        }

        for i in patches:
            with open(i) as _input:
                _recipe_match = self._get_recipe(_items, i)
                if _recipe_match:
                    _recipe_match = _recipe_match[0]
                else:
                    continue  # pragma: no cover
                try:
                    for m in RegexRpl.finditer(r'^Upstream-Status:\s*(?P<class>.*)', _input.read(), flags=regex.regex.MULTILINE):
                        for k, v in _valid_class.items():
                            if m.group('class').strip().startswith(k) and not RegexRpl.match(v, m.group('class')):
                                res += self.finding(_recipe_match.Origin,
                                                    _recipe_match.InFileLine)
                except UnicodeDecodeError:  # pragma: no cover
                    pass  # pragma: no cover
        return res
