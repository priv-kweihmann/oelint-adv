from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.constants import CONSTANTS


class VarQuoted(Rule):
    def __init__(self):
        super().__init__(id='oelint.append.protvars',
                         severity='error',
                         message='Variable \'{VAR}\' shouldn\'t be set as part of a bbappend',
                         onlyappend=True,
                         appendix=CONSTANTS.VariablesProtectedAppend)

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in [x for x in items if x.VarName in CONSTANTS.VariablesProtectedAppend]:
            if i.VarOp not in [' ??= ', ' ?= '] and i.Flag not in ['vardeps', 'vardepsexclude', 'vardepvalue', 'vardepvalueexclude']:
                res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.replace(
                    '{VAR}', i.VarName), appendix=i.VarName)
        return res
