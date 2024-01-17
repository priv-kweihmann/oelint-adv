from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarPkgSpecific(Rule):
    def __init__(self) -> None:
        self.needles = ['RDEPENDS', 'RRECOMMENDS', 'RSUGGESTS', 'RCONFLICTS', 'RPROVIDES', 'RREPLACES',
                        'FILES', 'pkg_preinst', 'pkg_postinst', 'pkg_prerm', 'pkg_postrm', 'ALLOW_EMPTY']
        super().__init__(id='oelint.vars.pkgspecific',
                         severity='error',
                         message='Variable {VAR} is package-specific and therefore it should be {VAR}{DEL}<known package name>',
                         appendix=self.needles)

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []

        if self.is_lone_append(stash, _file):
            return res

        _packages = stash.GetValidPackageNames(_file)
        items: List[Variable] = stash.GetItemsFor(filename=_file,
                                                  classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR,
                                                  attributeValue=self.needles)
        if not items:
            return res
        delimiter = items[-1].OverrideDelimiter
        for i in items:
            _machine = []
            if i.GetMachineEntry():
                _machine = [i.GetMachineEntry(), stash.ExpandTerm(_file, i.GetMachineEntry())]
            if not _machine or not any(x in _packages for x in _machine):
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(self.Msg, VAR=i.VarName, DEL=delimiter), appendix=i.VarName)
        return res
