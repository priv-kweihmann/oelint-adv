from operator import attrgetter

from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.helper_files import get_scr_components
from oelint_adv.parser import INLINE_BLOCK


class VarSRCUriGitTag(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.srcuriappend",
                         severity="error",
                         message="Use SRC_URI_append otherwise this will override weak defaults by inherit")

    def check(self, _file, stash):
        res = []
        inherits = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="inherit")
        if not inherits:
            return res

        items = [x for x in stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                            attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")]
        for i in items:
            if any([i.Flag.endswith(x) for x in ["md5sum", "sha256sum"]]):
                # These are just the hashes
                continue
            if i.VarOp in [" += "]:
                res += self.finding(i.Origin, i.InFileLine)
        return res
