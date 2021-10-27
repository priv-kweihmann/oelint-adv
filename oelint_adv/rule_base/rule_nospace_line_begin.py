from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Function
from oelint_parser.cls_item import PythonBlock


class NoSpaceBeginningRule(Rule):
    def __init__(self):
        super().__init__(id='oelint.spaces.linebeginning',
                         severity='warning',
                         message='Line shall not begin with a space')

    def __getMatches(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw and i.Raw.startswith(' '):
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
            if isinstance(i, PythonBlock) or isinstance(i, Function):
                continue  # pragma: no cover
            i.RealRaw = i.RealRaw.lstrip(' ')
            i.Raw = i.Raw.lstrip(' ')
            res.append(_file)
        return res
