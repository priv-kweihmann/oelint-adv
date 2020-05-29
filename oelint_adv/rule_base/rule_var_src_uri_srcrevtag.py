from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.helper_files import get_scr_components
from oelint_adv.parser import INLINE_BLOCK


class VarSRCUriSRCREVTag(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.srcurisrcrevtag",
                         severity="error",
                         message="'tag' in SRC_URI and a SRCREV for the same component doesn't compute")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
        for i in items:
            if any([i.Flag.endswith(x) for x in ["md5sum", "sha256sum"]]):
                # These are just the hashes
                continue
            lines = [y.strip('"') for y in i.get_items() if y]
            for x in lines:
                if x == INLINE_BLOCK:
                    continue
                _url = get_scr_components(x)
                if _url["scheme"] in ["git"] and "tag" in _url["options"]:
                    _srcrevs = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="SRCREV")
                    if "name" in _url["options"]:
                        _srcrevs = [x for x in _srcrevs if _url["options"]["name"] in x.SubItems]
                    else:
                        _srcrevs = [x for x in _srcrevs if not x.SubItems]
                    if any(_srcrevs):
                        res += self.finding(i.Origin, i.InFileLine)
        return res
