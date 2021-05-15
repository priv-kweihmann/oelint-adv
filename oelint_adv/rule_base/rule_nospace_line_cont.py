from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Comment
import re


class NoSpaceRuleCont(Rule):
    def __init__(self):
        super().__init__(id="oelint.spaces.linecont",
                         severity="error",
                         message="No spaces after line continuation")

    def __getMatches(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if isinstance(i, Comment):
                continue
            if i.Raw: # pragma: no cover
                if re.search(r"\\\s+\n", i.Raw):
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
            i.RealRaw = re.sub(r"\\\s+\n", "\\\n", i.RealRaw)
            i.Raw = re.sub(r"\\\s+\n", "\\\n", i.Raw)
            res.append(_file)
        return res
