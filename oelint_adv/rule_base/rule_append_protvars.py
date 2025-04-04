from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule, Classification


class VarQuoted(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.append.protvars',
                         severity='error',
                         message='Variable \'{VAR}\' shouldn\'t be set as part of a bbappend',
                         run_on=[Classification.BBAPPEND],
                         appendix=CONSTANTS.GetByPath('variables/protected-append'))

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in [x for x in items if x.VarName in CONSTANTS.GetByPath('variables/protected-append')]:
            if i.VarOp.strip() not in ['??=', '?=']:
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.replace('{VAR}', i.VarName), appendix=i.VarName)
        return res
