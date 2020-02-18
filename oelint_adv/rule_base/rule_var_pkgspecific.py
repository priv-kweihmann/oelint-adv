from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarQuoted(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.pkgspecific",
                         severity="error",
                         message="Variable {VAR} is package-specific and therefore it should be {VAR}_${PN}")

    def check(self, _file, stash):
        res = []
        needles = ['RDEPENDS', 'RRECOMMENDS', 'RSUGGESTS', 'RCONFLICTS', 'RPROVIDES', 'RREPLACES',
                   'FILES', 'pkg_preinst', 'pkg_postinst', 'pkg_prerm', 'pkg_postrm', 'ALLOW_EMPTY']
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if i.VarName == "inherit":
                continue
            if i.VarName in needles:
                res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.replace("{VAR}", i.VarName))
        return res
