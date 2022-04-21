from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.helper_files import get_scr_components


class VarPnBpnUsage(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.pbpusage',
                         severity='error',
                         message='${BP} should be used instead of ${P}')

    def __getMatches(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        needles = ['SRC_URI', 'S']
        for i in [x for x in items if x.VarName in needles]:
            for x in i.get_items():
                if i.VarName == 'SRC_URI':
                    _haystack = get_scr_components(x)['src']
                else:
                    _haystack = x
                if '${P}' in _haystack:
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
            i.RealRaw = i.RealRaw.replace('${P}', '${BP}')
            i.Raw = i.Raw.replace('${P}', '${BP}')
            res.append(_file)
        return res
