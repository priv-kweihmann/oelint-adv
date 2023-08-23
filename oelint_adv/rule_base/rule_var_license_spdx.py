from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule


class LicenseSDPX(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.licensesdpx',
                         severity='warning',
                         message='LICENSE is not a valid OpenEmbedded SPDX expression')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        for i in [x for x in items if x.VarName == 'LICENSE']:
            if (('|' in i.VarValueStripped and ' | ' not in i.VarValueStripped) or
               ('&' in i.VarValueStripped and ' & ' not in i.VarValueStripped)):
                res += self.finding(i.Origin, i.InFileLine)
        return res
