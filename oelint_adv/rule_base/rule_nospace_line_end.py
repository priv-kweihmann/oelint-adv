import re
from copy import deepcopy

from oelint_adv.cls_rule import Rule


class NoSpaceTrailingRule(Rule):
    def __init__(self):
        super().__init__(id="oelint.spaces.lineend",
                         severity="warning",
                         message="Line shall not end with a space")

    def __getMatches(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            _linecnt = 0
            for line in i.Raw.split("\n"):
                if line.endswith(" "):
                    _i = deepcopy(i)
                    _i.Line = i.Line + _linecnt
                    res.append(_i)
                _linecnt += 1
        return res

    def check(self, _file, stash):
        res = []
        for i in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, i.InFileLine)
        return res

    def fix(self, _file, stash):
        res = []
        for i in self.__getMatches(_file, stash):
            i.Raw = re.sub(r"\s{2,}\n", "\n", i.Raw)
            res.append(_file)
        return res
