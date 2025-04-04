import os
from typing import List, Tuple

import regex  # noqa: I900
from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule, Classification


class FilePatchIsUpstreamStatus(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.file.upstreamstatus',
                         severity='info',
                         run_on=[Classification.BBAPPEND, Classification.RECIPE],
                         message='Patch \'{FILE}\' should contain an Upstream-Status entry')

    def _get_recipe(self, items, path):
        # Find matching SRC_URI assignment
        return [x for x in items if x.VarValue.find(os.path.basename(path)) != -1]

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        patches = stash.GetFiles(_file, '*.patch')
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')

        _valid_class = {
            'Pending': r'Pending',
            'Submitted': r'Submitted(\s+\[.*\])*',
            'Accepted': r'Accepted',
            'Denied': r'Denied',
            'Backport': r'Backport',
            'Inappropriate': r'Inappropriate(\s+\[.*\])*',
            'Inactive-Upstream': r'Inactive-Upstream(\s+\[.*\])*',
        }
        for i in patches:
            with open(i) as _input:
                found = False
                _recipe_match = self._get_recipe(_items, i)
                if _recipe_match:
                    _recipe_match = _recipe_match[0]
                else:
                    continue  # pragma: no cover
                try:
                    cnt = _input.read()
                    for m in RegexRpl.finditer(r'^Upstream-Status:\s*(?P<class>.*)', cnt, flags=regex.regex.MULTILINE):
                        found = True
                        if not any(RegexRpl.match(v, m.group('class')) for k, v in _valid_class.items()):
                            _msg = 'Upstream-Status in \'{FILE}\' doesn\'t pick from valid classifiers {cls}'.format(
                                FILE=os.path.basename(i), cls=','.join(sorted(_valid_class.keys())),
                            )
                            res += self.finding(_recipe_match.Origin,
                                                _recipe_match.InFileLine,
                                                override_msg=_msg)
                    if not found:
                        res += self.finding(_recipe_match.Origin,
                                            _recipe_match.InFileLine,
                                            self.Msg.replace('{FILE}', os.path.basename(i)))
                except UnicodeDecodeError:  # pragma: no cover
                    pass  # pragma: no cover
        return res
