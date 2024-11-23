from typing import List, Tuple

from oelint_parser.cls_item import FlagAssignment, Function
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class TaskNetwork(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.task.network',
                         severity='warning',
                         message='Task \'{FUNC}\' uses the network flag, that can lead to unpredictable results',
                         valid_from_release='kirkstone')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        task_names = {x.FuncName for x in stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER)}
        task_names.update(CONSTANTS.FunctionsKnown)
        for item in stash.GetItemsFor(filename=_file,
                                      classifier=FlagAssignment.CLASSIFIER,
                                      attribute=FlagAssignment.ATTR_NAME,
                                      attributeValue=task_names):
            if item.VarName in ['do_fetch']:
                continue
            if item.Flag in ['network'] and item.ValueStripped not in ['0']:
                res += self.finding(item.Origin, item.InFileLine,
                                    self.Msg.replace('{FUNC}', item.VarName))
        return res
