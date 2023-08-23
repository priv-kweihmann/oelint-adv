from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable


class VarAppendOperation(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.appendop',
                         severity='error',
                         message='Use \'{a}\' instead of \'{b}\' as it overwrites \'{c}\'')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        _names = {x.VarName for x in items if x.VarName != 'inherit'}
        for name in _names:
            _weakest = [x for x in items if x.VarName == name and x.VarOp.strip() == '??=']
            _weak = [x for x in items if x.VarName == name and x.VarOp.strip() == '?=']
            _items = [x for x in items if x.VarName == name and x not in _weakest + _weak and x.VarOp.strip() in ['.=', '+=']]
            for i in _items:
                override_delimiter = i.OverrideDelimiter
                if any(_weakest):
                    res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format(
                        a='{od}append'.format(od=override_delimiter), b=i.VarOp, c=_weakest[0].Raw))
                elif any(x.Line > i.Line for x in _weak):
                    res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format(
                        a='{od}append'.format(od=override_delimiter), b=i.VarOp, c=_weak[0].Raw))
            _items = [x for x in items if x.VarName == name and x not in _weakest + _weak and x.VarOp.strip() in ['=.', '=+']]
            for i in _items:
                override_delimiter = i.OverrideDelimiter
                if any(_weakest):
                    res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format(
                        a='{od}prepend'.format(od=override_delimiter), b=i.VarOp, c=_weakest[0].Raw))
                elif any(x.Line > i.Line for x in _weak):
                    res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format(
                        a='{od}prepend'.format(od=override_delimiter), b=i.VarOp, c=_weak[0].Raw))
        return res
