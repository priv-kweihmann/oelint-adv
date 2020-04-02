from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule

class VarDescSame(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.descriptionsame",
                         severity="warning",
                         message="'DESCRIPTION' is the same a 'SUMMARY' - it can be removed then")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="DESCRIPTION")
        items_sum = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                      attribute=Variable.ATTR_VAR, attributeValue="SUMMARY")
        for i in items:
            _same = [x for x in items_sum if x.VarValueStripped ==
                     i.VarValueStripped]
            if any(_same):
                res += self.finding(i.Origin, i.InFileLine)
        return res
