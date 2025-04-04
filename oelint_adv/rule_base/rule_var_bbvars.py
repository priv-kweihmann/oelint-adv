from typing import List, Tuple

from oelint_parser.cls_item import Variable, Inherit
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule, Classification


class VarQuoted(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.bbvars',
                         severity='warning',
                         run_on=[Classification.BBAPPEND, Classification.BBCLASS, Classification.RECIPE],
                         message='Variable \'{VAR}\' should be set on a disto/layer or local.conf level, not in a recipe',
                         appendix=CONSTANTS.GetByPath('variables/protected'))

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file,
                                                  classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR,
                                                  attributeValue=CONSTANTS.GetByPath('variables/protected'))
        inherits: List[Inherit] = stash.GetItemsFor(filename=_file,
                                                    classifier=Inherit.CLASSIFIER,
                                                    attribute=Inherit.ATTR_STATEMENT,
                                                    attributeValue="INHERIT")

        for i in items:
            if i.Origin in stash.GetConfFiles():
                continue  # pragma: no cover
            if i.VarOp.strip() not in ['??=', '?=']:
                res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.replace(
                    '{VAR}', i.VarName), appendix=i.VarName)
        for i in inherits:
            if i.Origin in stash.GetConfFiles():
                continue  # pragma: no cover
            res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.replace(
                '{VAR}', 'INHERIT'), appendix='INHERIT')
        return res
