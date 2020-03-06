import re

from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.helper_files import get_valid_package_names, get_valid_named_resources


class VarPnBpnUsage(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.machinespecific",
                         severity="error",
                         message="'{}' is set machine specific ['{}'], but a matching COMPATIBLE_MACHINE entry is missing")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        _packages = get_valid_package_names(stash, _file)
        _named_res = get_valid_named_resources(stash, _file)
        for i in items:
            _machine = i.GetMachineEntry()
            if not _machine or _machine in _packages or _machine in _named_res:
                continue
            _comp = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                      attribute=Variable.ATTR_VAR, attributeValue="COMPATIBLE_MACHINE")
            if not any(_comp):
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(i.VarName, _machine))
                continue
            _vals = [x.VarValueStripped.lstrip(
                "|") for x in _comp if x.VarValueStripped]
            if not any(re.match(v, _machine) or (_machine == "qemuall" and "qemu" in v) for v in _vals):
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(i.VarName, _machine))
        return res
