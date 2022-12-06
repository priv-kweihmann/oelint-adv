import os

from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable


class VarBugtrackerIsUrl(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.fileextrapaths',
                         severity='warning',
                         message='\'FILESEXTRAPATHS\' shouldn\'t be used in a bb file')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        for i in items:
            if i.VarName in ['FILESEXTRAPATHS']:
                _, ext = os.path.splitext(i.Origin)
                if ext == '.bb':
                    res += self.finding(i.Origin, i.InFileLine)
        return res
