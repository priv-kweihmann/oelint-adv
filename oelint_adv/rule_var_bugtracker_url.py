from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import *
from urllib.parse import urlparse


class VarBugtrackerIsUrl(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.bugtrackerisurl",
                         severity="warning",
                         message="'BUGTRACKER' should be an URL")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="BUGTRACKER")
        for i in items:
            val = i.VarValue.replace("\"", "").strip()
            try:
                result = urlparse(val)
                if not result.scheme or not result.netloc:
                    raise Exception()
            except:
                res += self.finding(i.Origin, i.InFileLine)
        return res
