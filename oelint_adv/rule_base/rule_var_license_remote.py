from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.helper_files import get_scr_components, expand_term


class VarLicenseRemoteFile(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.licenseremotefile",
                         severity="warning",
                         message="License-File should be a remote file")

    def check(self, _file, stash):
        res = []
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue="LIC_FILES_CHKSUM")
        _var_whitelist = ["${WORKDIR}", "${S}", "${B}"]
        for i in _items:
            components = get_scr_components(expand_term(stash, _file, i.VarValueStripped))
            if any(components) and components["scheme"] == "file":
                _clean = components["src"]
                for x in _var_whitelist:
                    _clean = _clean.replace(x, "")
                if "${" in _clean:
                    res += self.finding(i.Origin, i.InFileLine)
        return res
