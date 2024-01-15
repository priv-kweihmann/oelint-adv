import os
from typing import List, Tuple

from oelint_parser.cls_item import Include
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class FileIncludeNotFound(Rule):
    def __init__(self):
        super().__init__(id='oelint.file.includenotfound',
                         severity='warning',
                         message='\'{FILE}\' was not found')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for item in stash.GetItemsFor(filename=_file,
                                      classifier=Include.CLASSIFIER):
            if item.Statement == 'include':
                _path = stash.ExpandTerm(_file, item.IncName)
                if not stash.FindLocalOrLayer(_path, os.path.dirname(item.Origin)):
                    res += self.finding(item.Origin, item.InFileLine,
                                        self.Msg.replace('{FILE}', item.IncName))
        return res
