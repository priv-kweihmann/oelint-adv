import re

from oelint_adv.cls_item import Function
from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarPnBpnUsage(Rule):
    def __init__(self):
        super().__init__(id="oelint.func.machinespecific",
                         severity="error",
                         message="'{}' is set machine specific ['{}'], but a matching COMPATIBLE_MACHINE entry is missing")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER,
                                  attribute=Function.ATTR_FUNCNAME)
        for i in items:
            _machine = i.GetMachineEntry()
            if not _machine:
                continue
            if i.FuncName in ['pkg_preinst', 'pkg_postinst', 'pkg_prerm', 'pkg_postrm'] and _machine.startswith("${PN}"):
                continue
            if _machine in ["ptest"]:
                # known exceptions
                continue
            _comp = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                      attribute=Variable.ATTR_VAR, attributeValue="COMPATIBLE_MACHINE")
            if not any(_comp):
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(i.FuncName, _machine))
                continue
            _vals = [x.VarValueStripped.lstrip(
                "|") for x in _comp if x.VarValueStripped]
            if not any(re.match(v, _machine) or (_machine == "qemuall" and "qemu" in v) for v in _vals):
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(i.FuncName, _machine))
        return res
