import re

from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_parser.helper_files import get_valid_package_names, get_valid_named_resources
from oelint_parser.const_vars import get_known_machines


class VarPnBpnUsage(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.specific",
                         severity="error",
                         message="'{}' is set specific to ['{}'], but isn't known from PACKAGES, MACHINE or resources",
                         onappend=False)

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        _comp = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER, 
                            attribute=Variable.ATTR_VAR, 
                            attributeValue="COMPATIBLE_MACHINE")
        _packages = get_valid_package_names(stash, _file)
        _named_res = get_valid_named_resources(stash, _file)
        for i in items:
            _machine = i.GetMachineEntry()
            if not _machine:
                continue
            if _machine in _packages or _machine in _named_res or _machine in get_known_machines():
                continue
            if _comp and re.match("".join(x.VarValueStripped for x in _comp), _machine):
                continue
            res += self.finding(i.Origin, i.InFileLine,
                                override_msg=self.Msg.format(i.VarName, _machine))
        return res
