from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.helper_files import get_scr_components
from oelint_adv.parser import INLINE_BLOCK


class VarSRCUriGitTag(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.srcurifile",
                         severity="warning",
                         message="First item of SRC_URI should not be a file:// fetcher, if multiple fetcher are used")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
        _fetcher = []
        for i in items:
            if any([i.Flag.endswith(x) for x in ["md5sum", "sha256sum"]]):
                # These are just the hashes
                continue
            lines = [y.strip('"') for y in i.get_items() if y]
            
            for x in lines:
                if x == INLINE_BLOCK:
                    _fetcher.append(("inline", i.InFileLine))
                    continue
                _url = get_scr_components(x)
                _fetcher.append((_url["scheme"], i.InFileLine))
        if _fetcher:
            if any(x[0] != "file" for x in _fetcher) and _fetcher[0][0] == "file":
                res += self.finding(i.Origin, _fetcher[0][1])
        return res
