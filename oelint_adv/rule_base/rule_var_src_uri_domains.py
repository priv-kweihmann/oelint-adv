from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.helper_files import get_scr_components, safe_linesplit


class VarSRCUriOptions(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.srcuridomains",
                         severity="warning",
                         message="Recipe is pulling from different domains, this will likely cause issues")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")

        _domains = set()
        for i in items:
            for u in [x.strip() for x in safe_linesplit(i.VarValueStripped)]:
                _url = get_scr_components(u)
                if _url["scheme"] and _url["scheme"] not in ["file"]:
                    _domains.add(_url["src"].split("/")[0])
        if len(_domains) > 1:
            res += self.finding(i.Origin, i.InFileLine)
        return res
