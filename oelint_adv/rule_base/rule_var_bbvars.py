from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.constants import CONSTANTS


class VarQuoted(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.bbvars',
                         severity='warning',
                         message='Variable \'{VAR}\' should be set on a disto/layer or local.conf level, not in a recipe',
                         appendix=CONSTANTS.VariablesProtected)

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in [x for x in items if x.VarName in CONSTANTS.VariablesProtected]:
            if i.VarOp not in [' ??= ', ' ?= ']:
                res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.replace(
                    '{VAR}', i.VarName), appendix=i.VarName)
        return res
