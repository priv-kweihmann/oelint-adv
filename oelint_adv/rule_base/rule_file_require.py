import os

from oelint_parser.cls_item import Include
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class FileRequireNotFound(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.file.requirenotfound',
                         severity='error',
                         message="'{FILE}' was not found")
        self._ignores = CONSTANTS.GetByPath('oelint-require-file-ignore')

    def check(self, _file: str, stash: Stash) -> list[Rule.Finding]:
        res = []
        for item in stash.GetItemsFor(filename=_file,
                                      classifier=Include.CLASSIFIER):
            if item.Statement == 'require':
                _path = stash.ExpandTerm(_file, item.IncName)
                if _path in self._ignores or item.IncName in self._ignores:
                    continue
                if not stash.FindLocalOrLayer(_path, os.path.dirname(item.Origin)):
                    res += self.finding(item.Origin, item.InFileLine,
                                        self.Msg.replace('{FILE}', item.IncName))
        return res
