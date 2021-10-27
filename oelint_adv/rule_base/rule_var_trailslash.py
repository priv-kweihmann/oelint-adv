from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_parser.helper_files import expand_term


class VarTrailingSlash(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.notrailingslash',
                         severity='error',
                         message='\'{a}\' must not end with a \'/\'')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        _needles = ['S', 'B', 'T', 'D']
        for i in items:
            if i.VarName not in _needles:
                continue
            _expanded = expand_term(stash, _file, i.VarValueStripped)
            if _expanded.endswith('/'):
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(a=i.VarName))
        return res
