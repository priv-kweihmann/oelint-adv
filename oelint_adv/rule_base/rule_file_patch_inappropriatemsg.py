import os
import re

from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.helper_files import get_files


class FilePatchIsUpstreamStatusInAppMsg(Rule):
    def __init__(self):
        super().__init__(id='oelint.file.inappropriatemsg',
                         severity='info',
                         message='Patch \'{FILE}\' with Upstream-Status Inappropriate has to have a reasoning appended in [], chosen from {choices}')

    def _get_recipe(self, items, path):
        # Find matching SRC_URI assignment
        return [x for x in items if x.VarValue.find(os.path.basename(path)) != -1]

    def check(self, _file, stash):
        res = []
        patches = get_files(stash, _file, '*.patch')
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')

        _valid_classifiers = [
            'oe-specific',
            'OE specific',
            'oe-core specific',
            'not author',
            'native',
            'licensing',
            'configuration',
            'enable feature',
            'disable feature',
            'bugfix .*',
            'embedded specific',
            'no upstream',
            'other',
        ]

        _valid_class = {
            'Inappropriate': r'Inappropriate\s+\[({a})\]'.format(a='|'.join(_valid_classifiers)),
        }

        for i in patches:
            with open(i) as _input:
                _recipe_match = self._get_recipe(_items, i)
                if _recipe_match:
                    _recipe_match = _recipe_match[0]
                else:
                    continue  # pragma: no cover
                try:
                    for m in re.finditer(r'^Upstream-Status:\s*(?P<class>.*)', _input.read(), re.MULTILINE):
                        for k, v in _valid_class.items():
                            if m.group('class').strip().startswith(k) and not re.match(v, m.group('class')):
                                res += self.finding(_recipe_match.Origin,
                                                    _recipe_match.InFileLine,
                                                    self.Msg.format(FILE=os.path.basename(i), choices=','.join(_valid_classifiers)))
                except UnicodeDecodeError:  # pragma: no cover
                    pass  # pragma: no cover
        return res
