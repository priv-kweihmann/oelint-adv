from difflib import SequenceMatcher

from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.constants import CONSTANTS
from oelint_parser.helper_files import get_valid_package_names


class VarMisspell(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.mispell',
                         severity='warning',
                         message='<FOO>')

    def get_best_match(self, item, _list, minconfidence=0.8):
        _dict = sorted([(SequenceMatcher(None, item, k).ratio(), k)
                        for k in _list], key=lambda x: x[0], reverse=True)
        if _dict and _dict[0][0] >= minconfidence:
            return _dict[0][1]
        return ''

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        _all = stash.GetItemsFor(filename=_file)
        for i in items:
            _cleanvarname = i.VarName
            for pkg in get_valid_package_names(stash, _file, strippn=True):
                if not pkg:
                    continue  # pragma: no cover
                if _cleanvarname.endswith(pkg):
                    _cleanvarname = ''.join(
                        _cleanvarname.rsplit(pkg, 1))  # pragma: no cover
            if _cleanvarname in CONSTANTS.VariablesKnown:
                continue
            _used = False
            for a in _all:
                if a == i:
                    continue
                if '${{{a}}}'.format(a=i.VarName) in a.Raw or 'getVar("{a}"'.format(a=i.VarName) in a.Raw:
                    _used = True
                    break
            if _used:
                continue
            _bestmatch = self.get_best_match(
                _cleanvarname, CONSTANTS.VariablesKnown)
            if _bestmatch:
                res += self.finding(i.Origin, i.InFileLine,
                                    '\'{a}\' is unknown, maybe you meant \'{b}\''.format(
                                        a=_cleanvarname, b=_bestmatch))
        return res
