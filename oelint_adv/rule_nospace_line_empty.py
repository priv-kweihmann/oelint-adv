from oelint_adv.cls_rule import Rule


class NoSpaceEmptyLineRule(Rule):
    def __init__(self):
        super().__init__(id="oelint.spaces.emptyline",
                         severity="warning",
                         message="Empty lines shall not contain spaces")

    def __getMatches(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw.strip("\n") and not i.Raw.strip():
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
            i.Raw = "\n"
            res.append(_file)
        return res
