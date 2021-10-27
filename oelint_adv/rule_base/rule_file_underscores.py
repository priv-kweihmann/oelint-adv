import os
import re

from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable


class FileNoSpaces(Rule):
    def __init__(self):
        super().__init__(id='oelint.file.underscores',
                         severity='error',
                         message='FOO',
                         onappend=False)

    def check(self, _file, stash):
        res = []
        _basename, _ext = os.path.splitext(os.path.basename(_file))
        if _ext in ['.bb']:  # pragma: no cover
            _image_install = any(stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                   attribute=Variable.ATTR_VAR, attributeValue='IMAGE_INSTALL'))
            _inherits = set()
            for inh in stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                         attribute=Variable.ATTR_VAR, attributeValue='inherit'):
                _inherits.update([x.strip() for x in re.split(
                    r'\s|,|\t|\x1b', inh.VarValue) if x])
            if _image_install or any(x in _inherits for x in ['core-image', 'image']):
                return res
            _sep = [x for x in _basename if x in ['_', '-']]
            _us = [x for x in _sep if x == '_']
            if len(_us) > 1:
                res += self.finding(_file, 1,
                                    override_msg='Filename should not contain more than one \'_\'')
            elif not _us or _sep[-1] != '_':
                res += self.finding(
                    _file, 1, override_msg='Filename should contain at least one \'_\' in the end')
        return res
