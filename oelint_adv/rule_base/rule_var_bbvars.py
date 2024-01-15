from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class VarQuoted(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.bbvars',
                         severity='warning',
                         message='Variable \'{VAR}\' should be set on a disto/layer or local.conf level, not in a recipe',
                         appendix=CONSTANTS.VariablesProtected)

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file,
                                                  classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR,
                                                  attributeValue=CONSTANTS.VariablesProtected)
        for i in items:
            if i.VarOp.strip() not in ['??=', '?=']:
                res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.replace(
                    '{VAR}', i.VarName), appendix=i.VarName)
        return res
