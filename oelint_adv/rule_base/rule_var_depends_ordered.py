from copy import deepcopy

from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarDependsOrdered(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.dependsordered",
                         severity="warning",
                         message="[R]DEPENDS entries should be ordered alphabetically")

    def __get_tuple_wildcard_index(self, _list, elem):
        for i in range(len(_list)):
            if _list[i][1] == elem:
                return i
        return -1

    def check(self, _file, stash):
        res = []
        for elem in ["DEPENDS", "RDEPENDS_${PN}"]:
            items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                      attribute=Variable.ATTR_VAR, attributeValue=elem)
            items = sorted(items, key=lambda x: x.Line)
            _findings = []
            for i in items:
                linenum = 0
                for line in i.VarValueStripped.replace(chr(0x1b), "").split("\n"):
                    for x in [x for x in line.split(" ") if x]:
                        _i = deepcopy(i)
                        _i.Line += linenum
                        _findings.append((_i, x))
                    linenum += 1
            _sorted = sorted(_findings, key=lambda tup: tup[1])
            for i in _sorted:
                if self.__get_tuple_wildcard_index(_sorted, i[1]) != \
                        self.__get_tuple_wildcard_index(_findings, i[1]):
                    res += self.finding(i[0].Origin, i[0].InFileLine)
        return res
