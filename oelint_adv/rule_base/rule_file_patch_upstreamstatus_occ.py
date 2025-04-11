import os
from typing import List, Tuple

import regex  # noqa: I900
from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule, Classification


class FilePatchUpstreamStatusOccurance(Rule):
    def __init__(self) -> None:
        self._valid_class = {
            'Pending': r'^Upstream-Status:\s*Pending',
            'Submitted': r'^Upstream-Status:\s*Submitted(\s+\[.*\])*',
            'Accepted': r'^Upstream-Status:\s*Accepted',
            'Denied': r'^Upstream-Status:\s*Denied',
            'Backport': r'^Upstream-Status:\s*Backport',
            'Inappropriate': r'^Upstream-Status:\s*Inappropriate(\s+\[.*\])*',
            'Inactive-Upstream': r'^Upstream-Status:\s*Inactive-Upstream(\s+\[.*\])*',
        }
        super().__init__(id='oelint.file.upstreamstatus_occurance',
                         severity='inactive',
                         run_on=[Classification.BBAPPEND, Classification.RECIPE],
                         message='Found {ID} set as Upstream-Status in patch \'{FILE}\'',
                         appendix=list(self._valid_class.keys()))

    def _get_recipe(self, items, path):
        # Find matching SRC_URI assignment
        return [x for x in items if x.VarValue.find(os.path.basename(path)) != -1]

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        patches = stash.GetFiles(_file, '*.patch')
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')

        for i in patches:
            with open(i) as _input:
                _recipe_match = self._get_recipe(_items, i)
                if _recipe_match:
                    _recipe_match = _recipe_match[0]
                else:
                    continue  # pragma: no cover
                try:
                    cnt = _input.read()
                    for k, v in self._valid_class.items():
                        for _ in RegexRpl.finditer(v, cnt, flags=regex.regex.MULTILINE):
                            res += self.finding(_recipe_match.Origin,
                                                _recipe_match.InFileLine,
                                                override_msg=self.Msg.format(ID=k, FILE=os.path.basename(i)),
                                                appendix=k)
                except UnicodeDecodeError:  # pragma: no cover
                    pass  # pragma: no cover
        return res
