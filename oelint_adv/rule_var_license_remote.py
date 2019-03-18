try:
    from .cls_rule import Rule
    from .cls_item import *
    from .helper_files import get_scr_components
except (SystemError, ImportError):
    from cls_rule import Rule
    from cls_item import *
    from helper_files import get_scr_components
from urllib.parse import urlparse
import os

class VarLicenseRemoteFile(Rule):
    def __init__(self):
        super().__init__(id = "oelint.var.licenseremotefile", 
                         severity="warning",
                         message="License-File should be a remote file")

    def check(self, _file, stash):
        res = []
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue="LIC_FILES_CHKSUM")
        for i in _items:
            components = get_scr_components(i.VarValue)
            if any(components) and components["proto"] == "file":
                res += self.finding(i.Origin, i.InFileLine)
        return res