from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.helper_files import expand_term
from oelint_parser.helper_files import get_valid_package_names


class VarPkgSpecific(Rule):
    def __init__(self):
        self.needles = ['RDEPENDS', 'RRECOMMENDS', 'RSUGGESTS', 'RCONFLICTS', 'RPROVIDES', 'RREPLACES',
                        'FILES', 'pkg_preinst', 'pkg_postinst', 'pkg_prerm', 'pkg_postrm', 'ALLOW_EMPTY']
        super().__init__(id='oelint.vars.pkgspecific',
                         severity='error',
                         message='Variable {VAR} is package-specific and therefore it should be {VAR}_${PN} or {VAR}:${PN}',
                         appendix=self.needles)

    def check(self, _file, stash):
        res = []

        if self.is_lone_append(stash, _file):
            return res

        _packages = list(get_valid_package_names(stash, _file))
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if i.VarName == 'inherit':
                continue
            if i.VarName in self.needles:
                _machine = []
                if i.GetMachineEntry():
                    _machine = [i.GetMachineEntry(), expand_term(
                        stash, _file, i.GetMachineEntry())]
                if not _machine or not any(x in _packages for x in _machine):
                    res += self.finding(i.Origin, i.InFileLine,
                                        override_msg=self.Msg.replace('{VAR}', i.VarName), appendix=i.VarName)
        return res
