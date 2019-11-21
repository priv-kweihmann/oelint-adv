from copy import deepcopy

from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarDependsSingleLine(Rule):
    def __init__(self):
        super().__init__(id="oelint.jetm.vars.dependssingleline",
                         severity="warning",
                         message="Each [R]DEPENDS entry should be put into a single line")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="DEPENDS")
        items += stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue="RDEPENDS_${PN}")
        for i in items:
            linenum = 0
            for line in i.VarValueStripped.split("\n"):
                _ent = [x for x in line.strip("\\").split(" ") if x.strip()]
                if len(_ent) > 1:
                    for _ in _ent[1:]:
                        _i = deepcopy(i)
                        _i.Line = i.Line + linenum
                        res += self.finding(_i.Origin, _i.InFileLine)
                linenum += 1
        return res
