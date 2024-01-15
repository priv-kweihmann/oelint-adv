from typing import List, Tuple

from oelint_parser.cls_item import Function, Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS
from oelint_parser.parser import INLINE_BLOCK
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class VarPnBpnUsage(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.func.specific',
                         severity='error',
                         message='\'{func}\' is set specific to [\'{machine}\'] or [\'{distro}\'], but isn\'t known from PACKAGES, MACHINE, DISTRO, or resources')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER,
                                  attribute=Function.ATTR_FUNCNAME)
        _comp = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR,
                                  attributeValue='COMPATIBLE_MACHINE')
        _packages = stash.GetValidPackageNames(_file)
        _valid_funcs = ['pkg_preinst',
                        'pkg_postinst', 'pkg_prerm', 'pkg_postrm']
        for b in ['pkg_preinst', 'pkg_postinst', 'pkg_prerm', 'pkg_postrm']:
            _valid_funcs += ['{a}-{b}'.format(a=b, b=p)
                             for p in _packages if p.strip() and p != INLINE_BLOCK]
        for i in items:
            _distro = i.GetDistroEntry()
            if _distro in CONSTANTS.DistrosKnown:
                continue

            _machine = i.GetMachineEntry()
            if not _machine or _machine in CONSTANTS.MachinesKnown:
                continue
            if i.FuncName in _valid_funcs:
                continue
            if _machine in ['ptest']:
                # known exceptions
                continue
            if _comp and RegexRpl.match(''.join(x.VarValueStripped for x in _comp), _machine):
                continue
            res += self.finding(i.Origin, i.InFileLine,
                                override_msg=self.Msg.format(func=i.FuncName, machine=_machine, distro=_distro))
        return res
