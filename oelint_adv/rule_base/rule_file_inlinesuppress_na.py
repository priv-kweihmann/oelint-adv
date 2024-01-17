from typing import List, Tuple

from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule
from oelint_adv.state import State


class FileNotApplicableInlineSuppression(Rule):
    def __init__(self, state: State = None):
        super().__init__(id='oelint.file.inlinesuppress_na',
                         severity='info',
                         message='Inline suppression for \'{id}\' is not needed')
        self._state = state

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        # special handling from main
        # do not announce any finding
        return []
