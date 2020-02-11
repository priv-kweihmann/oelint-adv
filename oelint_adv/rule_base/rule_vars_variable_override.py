import os

from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarOverride(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.override",
                         severity="error",
                         message="<FOO>")

    def check(self, _file, stash):
        res = []
        __varnames = [x.VarName for x in stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)]
        for v in __varnames:
            if v == "inherit":
                # This will be done by another rule
                continue
            items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue=v)
            items = sorted(items, key=lambda x: x.Line, reverse=False)
            for sub in [x.SubItem for x in items]:
                _items = [x for x in items if x.SubItem == sub and not x.IsAppend()]
                if len(_items) > 1:
                    _files = list(set([os.path.basename(x.Origin) for x in _items]))
                    res += self.finding(_items[0].Origin, _items[0].InFileLine,
                                        "Variable '{}' is set by {}".format(
                                        v, ",".join(_files)))
        return res
