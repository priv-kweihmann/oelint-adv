from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.constants import CONSTANTS


class VarsOrder(Rule):
    def __init__(self):
        super().__init__(id='oelint.var.order',
                         severity='warning',
                         message='<FOO>',
                         appendix=[self.__cleanname(x) for x in CONSTANTS.VariablesOrder])

    def __cleanname(self, _input):
        return _input.replace('$', '').replace('{', '').replace('}', '')

    def check(self, _file, stash):
        res = []
        _files = {item.Origin for item in stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)}
        for _single_file in _files:
            items = stash.GetItemsFor(
                filename=_single_file, classifier=Variable.CLASSIFIER, nolink=True)
            for item in items:
                _func_before = sorted(
                    [x for x in items if x.Line < item.Line and x.VarName in CONSTANTS.VariablesOrder], key=lambda x: x.Line, reverse=True)
                if any(_func_before):
                    _func_before = _func_before[0]
                    if item.VarName not in CONSTANTS.VariablesOrder:
                        continue
                    if CONSTANTS.VariablesOrder.index(item.VarName) < CONSTANTS.VariablesOrder.index(_func_before.VarName):
                        res += self.finding(item.Origin, item.InFileLine,
                                            '\'{a}\' should be placed before \'{b}\''.format(
                                                a=item.VarName, b=_func_before.VarName), appendix=self.__cleanname(item.VarName))
        return res
