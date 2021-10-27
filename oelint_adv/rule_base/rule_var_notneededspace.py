import re

from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarSectionLowercase(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.notneededspace',
                         severity='info',
                         message='Space at the beginning of the var is not needed')

    def __getMatches(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in [x for x in items if 'append' not in x.SubItems]:
            if i.VarValueStripped.startswith(' '):
                res.append(i)
        return res

    def check(self, _file, stash):
        res = []
        for i in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, i.InFileLine)
        return res

    def fix(self, _file, stash):
        res = []
        for i in self.__getMatches(_file, stash):
            i.RealRaw = re.sub(r'"\s+', '"', i.RealRaw) + '\n'
            i.Raw = re.sub(r'"\s+', '"', i.Raw) + '\n'
            i.VarValue = re.sub(r'"\s+', '"', i.VarValue) + '\n'
            res.append(_file)
        return res
