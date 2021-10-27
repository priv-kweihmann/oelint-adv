import os

from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Include
from oelint_parser.helper_files import expand_term
from oelint_parser.helper_files import find_local_or_in_layer


class FileRequireNotFound(Rule):
    def __init__(self):
        super().__init__(id='oelint.file.requirenotfound',
                         severity='error',
                         message='\'{FILE}\' was not found')

    def check(self, _file, stash):
        res = []
        for item in stash.GetItemsFor(filename=_file,
                                      classifier=Include.CLASSIFIER):
            if item.Statement == 'require':
                _path = expand_term(stash, _file, item.IncName)
                if not find_local_or_in_layer(_path, os.path.dirname(item.Origin)):
                    res += self.finding(item.Origin, item.InFileLine,
                                        self.Msg.replace('{FILE}', item.IncName))
        return res
