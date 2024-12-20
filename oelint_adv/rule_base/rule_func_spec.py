from typing import List, Tuple

from oelint_parser.cls_item import Function, Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class VarPnBpnUsage(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.func.specific',
                         severity='error',
                         message='\'{func}\' is set specific to [\'{b}\'], but isn\'t known from PACKAGES, MACHINE, DISTRO')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER,
                                  attribute=Function.ATTR_FUNCNAME)
        _comp = ''.join(x.VarValueStripped for x in stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                                      attribute=Variable.ATTR_VAR,
                                                                      attributeValue='COMPATIBLE_MACHINE'))
        _packages = stash.GetValidPackageNames(_file)
        _machines = CONSTANTS.MachinesKnown
        _distros = CONSTANTS.DistrosKnown
        _builtin_funcs = ['pkg_preinst', 'pkg_postinst', 'pkg_prerm', 'pkg_postrm', 'ptest']
        _operations = ['append', 'prepend', 'remove']
        for i in items:
            for sub in i.SubItems:
                if sub in _operations:
                    continue
                if sub in _distros:
                    continue
                if sub in _packages:
                    continue
                if sub in _machines:
                    continue
                if sub in _builtin_funcs:
                    continue
                if _comp and RegexRpl.match(_comp, sub):
                    continue
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(func=i.FuncName, b=sub))
        return res
