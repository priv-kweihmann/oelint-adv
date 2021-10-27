import re

from oelint_adv.cls_rule import Rule


class NoSpaceTrailingRule(Rule):
    def __init__(self):
        super().__init__(id='oelint.spaces.lineend',
                         severity='warning',
                         message='Line shall not end with a space')

    def __getMatches(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            _linecnt = 0
            for line in i.Raw.split('\n'):
                if line.endswith(' '):
                    res.append((i, i.Line + _linecnt))
                _linecnt += 1
        return res

    def check(self, _file, stash):
        res = []
        for i in self.__getMatches(_file, stash):
            res += self.finding(i[0].Origin, i[1])
        return res

    def fix(self, _file, stash):
        res = []
        for i in self.__getMatches(_file, stash):
            i.RealRaw = re.sub(r'\s{2,}\n', '\n', i[0].RealRaw)
            i.Raw = re.sub(r'\s{2,}\n', '\n', i[0].Raw)  # pragma: no cover
            res.append(_file)  # pragma: no cover
        return res  # pragma: no cover
