from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class VarPnBpnUsage(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.specific',
                         severity='error',
                         message='\'{a}\' is set specific to [\'{b}\'], but isn\'t known from PACKAGES, MACHINE, DISTRO or resources',
                         onappend=False)

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        _comp = ''.join(x.VarValueStripped for x in stash.Reduce(items, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR,
                                                                 attributeValue='COMPATIBLE_MACHINE'))
        _packages = stash.GetValidPackageNames(_file)
        _named_res = stash.GetValidNamedResources(_file)
        for i in items:
            _distro = []
            if i.GetDistroEntry():
                _distro = [i.GetDistroEntry(), stash.ExpandTerm(_file, i.GetDistroEntry())]
            if any(x in _packages for x in _distro) or any(x in _named_res for x in _distro):  # pragma: no cover
                continue  # pragma: no cover
            if any(x in CONSTANTS.DistrosKnown for x in _distro):
                continue

            _machine = []
            if i.GetMachineEntry():
                _machine = [i.GetMachineEntry(), stash.ExpandTerm(_file, i.GetMachineEntry())]
            if not _machine:
                continue
            if any(x in _packages for x in _machine):
                continue
            if any(x in _named_res for x in _machine):
                continue
            if any(x in CONSTANTS.MachinesKnown for x in _machine):
                continue
            if _comp:
                if any(RegexRpl.match(_comp, x) for x in _machine):
                    continue
            res += self.finding(i.Origin, i.InFileLine,
                                override_msg=self.Msg.format(a=i.VarName, b=_machine[0]))
        return res
