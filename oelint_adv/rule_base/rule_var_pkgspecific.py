from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.helper_files import get_valid_package_names


class VarPkgSpecific(Rule):
    def __init__(self):
        self.needles = ['RDEPENDS', 'RRECOMMENDS', 'RSUGGESTS', 'RCONFLICTS', 'RPROVIDES', 'RREPLACES',
                   'FILES', 'pkg_preinst', 'pkg_postinst', 'pkg_prerm', 'pkg_postrm', 'ALLOW_EMPTY']
        super().__init__(id="oelint.vars.pkgspecific",
                         severity="error",
                         message="Variable {VAR} is package-specific and therefore it should be {VAR}_${PN}",
                         appendix=self.needles)

    def check(self, _file, stash):
        res = []
        
        _packages = get_valid_package_names(stash, _file)
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if i.VarName == "inherit":
                continue
            if i.VarName in self.needles:
                _machine = i.GetMachineEntry()
                if not _machine or _machine not in _packages:
                    res += self.finding(i.Origin, i.InFileLine,
                                        override_msg=self.Msg.replace("{VAR}", i.VarName), appendix=i.VarName)
        return res
