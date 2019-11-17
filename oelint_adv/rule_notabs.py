from oelint_adv.cls_rule import Rule
import re


class NoTabs(Rule):
    def __init__(self):
        super().__init__(id="oelint.tabs.notabs",
                         severity="warning",
                         message="Don't use tabs use spaces")

    def __getMatches(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw and "\t" in i.Raw:
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
            i.Raw = re.sub(r"\t", "    ", i.Raw)
            res.append(_file)
        return res
