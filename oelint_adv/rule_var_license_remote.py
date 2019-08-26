from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import *
from oelint_adv.helper_files import get_scr_components
from urllib.parse import urlparse
import os


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
            components = get_scr_components(i.VarValue)
            if any(components) and components["proto"] == "file":
                if "name" in components:
                    if "${" in components["name"]:
                        res += self.finding(i.Origin, i.InFileLine)
        return res
