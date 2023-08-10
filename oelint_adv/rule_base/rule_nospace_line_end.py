from oelint_adv.cls_rule import Rule
from oelint_parser.rpl_regex import RegexRpl


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
                    res.append((i, i.InFileLine + _linecnt))
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
            i[0].RealRaw = RegexRpl.sub(r'\s+\n', '\n', i[0].RealRaw)
            i[0].Raw = RegexRpl.sub(r'\s+\n', '\n', i[0].Raw)
            res.append(_file)
        return res
