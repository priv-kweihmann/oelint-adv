from oelint_adv.cls_rule import Rule
import re


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
                if line.endswith("  "):
                    res.append(i)
                _linecnt += 1
        return res

    def check(self, _file, stash):
        res = []
        for i in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, i.InFileLine + _linecnt)
        return res

    def fix(self, _file, stash):
        res = []
        for i in self.__getMatches(_file, stash):
            i.Raw = re.sub(r"\s{2,}\n", "\n", i.Raw)
            res.append(_file)
        return res
