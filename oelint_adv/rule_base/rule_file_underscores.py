import os

from oelint_adv.cls_rule import Rule
from oelint_parser.helper_files import is_image
from oelint_parser.helper_files import is_packagegroup


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
            if is_packagegroup(stash, _file) or is_image(stash, _file):
                return []
            _sep = [x for x in _basename if x in ['_', '-']]
            _us = [x for x in _sep if x == '_']
            if len(_us) > 1:
                res += self.finding(_file, 1,
                                    override_msg='Filename should not contain more than one \'_\'')
            elif not _us or _sep[-1] != '_':
                res += self.finding(
                    _file, 1, override_msg='Filename should contain at least one \'_\' in the end')
        return res
