from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.helper_files import get_scr_components


class VarLicenseRemoteFile(Rule):
    def __init__(self):
        super().__init__(id="oelint.var.licenseremotefile",
                         severity="warning",
                         message="License-File should be a remote file")

    def check(self, _file, stash):
        res = []
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue="LIC_FILES_CHKSUM")
        for i in _items:
            components = get_scr_components(i.VarValueStripped)
            if any(components) and components["scheme"] == "file":
                if "${" in components["src"]:
                    res += self.finding(i.Origin, i.InFileLine)
        return res
