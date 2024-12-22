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
            subs = [(x, stash.ExpandTerm(_file, x)) for x in i.SubItems]
            for subitem in subs:
                sub, expanded = subitem
                if (expanded in _operations) or (sub in _operations):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if (expanded in _distros) or (sub in _distros):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if (expanded in _packages) or (sub in _packages):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if (expanded in _machines) or (sub in _machines):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if (expanded in _builtin_funcs) or (sub in _builtin_funcs):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if _comp and (RegexRpl.match(_comp, expanded) or RegexRpl.match(_comp, sub)):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(func=i.FuncName, b=sub))
        return res
