from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import *


class VarHomepagePrefix(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.homepageprefix",
                         severity="warning",
                         message="'HOMEPAGE' should start with 'http://' or 'https://'")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="HOMEPAGE")
        for i in items:
            tmp = i.VarValue.strip('"').strip()
            if not any([x for x in ["https://", "http://"] if tmp.startswith(x)]):
                res += self.finding(i.Origin, i.InFileLine)
        return res
