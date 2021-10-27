import re

from oelint_adv.cls_rule import Rule


class NoTabs(Rule):
    def __init__(self):
        super().__init__(id='oelint.tabs.notabs',
                         severity='warning',
                         message='Don\'t use tabs use spaces')

    def __getMatches(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw and '\t' in i.Raw:
                res.append(i)
        return res

    def check(self, _file, stash):
        res = []
        for i in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, i.InFileLine)
        return res

    def fix(self, _file, stash):  # pragma: no cover
        res = []  # pragma: no cover
        for i in self.__getMatches(_file, stash):  # pragma: no cover
            i.RealRaw = re.sub(r'\t', '    ', i.RealRaw)  # pragma: no cover
            i.Raw = re.sub(r'\t', '    ', i.Raw)  # pragma: no cover
            res.append(_file)  # pragma: no cover
        return res  # pragma: no cover
