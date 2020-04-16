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
            _items = {}
            for i in items:
                for x in [y for y in i.get_items() if y]:
                    machine_mods = i.SubItems
                    machine_mods_cleaned = "_".join(
                        sorted([x for x in machine_mods if x not in ["append", "prepend", "remove"]]))
                    if machine_mods_cleaned not in _items:
                        _items[machine_mods_cleaned] = []
                    _operations = i.AppendOperation()
                    if x in _items[machine_mods_cleaned]:
                        if x == "!!!inlineblock!!!":
                            continue
                        if not any([x in ["append", "prepend", " += ", " =+ "] for x in _operations]):
                            _items[machine_mods_cleaned] = [x]
                        else:
                            res += self.finding(i.Origin, i.InFileLine,
                                                "Item '{}' was added multiple times to {}".format(x, c))
                    else:
                        if any([x in ["append", "prepend", " += ", " =+ "] for x in _operations]):
                            _items[machine_mods_cleaned].append(x)
                        elif "remove" in _operations:
                            if x in _items[machine_mods_cleaned]:
                                _items[machine_mods_cleaned].remove(x)
                        else:
                            _items[machine_mods_cleaned] = [x]
        return res
