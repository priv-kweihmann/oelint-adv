from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.const_vars import KNOWN_VARS
from difflib import SequenceMatcher


class VarMisspell(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.mispell",
                         severity="warning",
                         message="<FOO>")

    def get_best_match(self, item, _list, minconfidence=0.8):
        _dict = sorted([(SequenceMatcher(None, item, k).ratio(), k)
                        for k in _list], key=lambda x: x[0], reverse=True)
        if _dict and _dict[0][0] >= minconfidence:
            return _dict[0][1]
        return ""

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)

        for i in items:
            if i.VarName in KNOWN_VARS:
                continue
            _bestmatch = self.get_best_match(i.VarName, KNOWN_VARS)
            if _bestmatch:
                res += self.finding(i.Origin, i.InFileLine,
                                    "'{}' is unknown, maybe you mean '{}'".format(
                                        i.VarName, _bestmatch))
        return res
