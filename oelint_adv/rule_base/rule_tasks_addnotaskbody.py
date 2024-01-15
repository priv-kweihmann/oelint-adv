from typing import List, Tuple

from oelint_parser.cls_item import Function, TaskAdd
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class TaskAddNoTaskBody(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.task.addnotaskbody',
                         severity='warning',
                         message='The added task \'{FUNC}\' is not existing or has no body')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for item in stash.GetItemsFor(filename=_file, classifier=TaskAdd.CLASSIFIER):
            if item.FuncName in CONSTANTS.FunctionsOrder:
                # not for builtin types
                continue
            if item.FuncName in [x.replace('do_', '', 1) for x in CONSTANTS.FunctionsOrder]:
                # not for builtin types - probed for missing prefix
                continue
            _ta = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER,
                                    attribute='FuncName')
            _filt = [x for x in _ta or [] if not isinstance(
                x, str) and x.FuncName == item.FuncName]
            _filt += [x for x in _ta or []
                      if not isinstance(x, str) and x.FuncName == 'do_' + item.FuncName]
            if not any(_filt):
                res += self.finding(item.Origin, item.InFileLine,
                                    self.Msg.replace('{FUNC}', item.FuncName))
            elif not any(x for x in _filt if x.FuncBodyStripped):
                res += self.finding(item.Origin, item.InFileLine,
                                    self.Msg.replace('{FUNC}', item.FuncName))
        return res
