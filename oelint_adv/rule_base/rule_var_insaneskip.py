from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable


class VarInsaneSkip(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.insaneskip',
                         severity='error',
                         message='INSANE_SKIP should be avoided at any cost')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        for i in [x for x in items if x.VarName == 'INSANE_SKIP']:
            res += self.finding(i.Origin, i.InFileLine)
        return res
