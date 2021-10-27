from oelint_adv.cls_rule import Rule
from oelint_parser.helper_files import get_layer_root


class FileNoSpaces(Rule):
    def __init__(self):
        super().__init__(id='oelint.file.nospaces',
                         severity='error',
                         message='Path to file contains spaces. Please remove them')

    def check(self, _file, stash):
        res = []
        _layer_root = get_layer_root(_file)
        _relpath = _file.replace(_layer_root, '').lstrip('/')
        if ' ' in _relpath:
            res += self.finding(_file, 1)
        return res
