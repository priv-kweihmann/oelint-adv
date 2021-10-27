from oelint_adv.cls_rule import Rule


class NewLineConsecutive(Rule):
    def __init__(self):
        super().__init__(id='oelint.newline.consecutive',
                         severity='warning',
                         message='Consecutive blank lines should be avoided')

    def __getMatches(self, _file, stash):
        res = {}
        items = stash.GetItemsFor(filename=_file)
        for _uniqname in {x.Origin for x in items}:
            res[_uniqname] = sorted(stash.GetItemsFor(
                filename=_uniqname, nolink=True), key=lambda x: x.InFileLine)
        return res

    def check(self, _file, stash):
        res = []
        for _, v in self.__getMatches(_file, stash).items():
            for index, value in enumerate(v):
                if index == 0:
                    continue
                if value.Raw == '\n' and v[index - 1].Raw == '\n':
                    res += self.finding(value.Origin, value.InFileLine)
        return res

    def fix(self, _file, stash):
        res = set()
        for f, v in self.__getMatches(_file, stash).items():
            for index, value in enumerate(v):
                if index == 0:
                    continue
                if value.RealRaw == '\n' and v[index - 1].RealRaw == '\n':
                    stash.Remove(value)
                    res.add(f)
        return list(res)
