from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarDuplicates(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.duplicate",
                         severity="warning",
                         message="<FOO>")

    def check(self, _file, stash):
        res = []
        for c in ["DEPENDS", "RDEPENDS_${PN}"]:
            items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                      attribute=Variable.ATTR_VAR, attributeValue=c)
            _items = []
            for i in items:
                for x in [y for y in i.VarValueStripped.split(" ") if y]:
                    if x in _items:
                        res += self.finding(i.Origin, i.InFileLine,
                                            "Item '{}' was added multiple time to {}".format(x, c))
                    else:
                        _items.append(x)
        return res
