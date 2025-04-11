from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule, Classification


class VarPnBpnUsage(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.specific',
                         severity='error',
                         message='\'{a}\' is set specific to [\'{b}\'], but isn\'t known from PACKAGES, MACHINE, DISTRO or resources',
                         run_on=[Classification.RECIPE, Classification.BBCLASS])

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        _comp = ''.join(x.VarValueStripped for x in stash.Reduce(items, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR,
                                                                 attributeValue='COMPATIBLE_MACHINE'))
        _packages = stash.GetValidPackageNames(_file)
        _named_res = stash.GetValidNamedResources(_file)
        _machines = CONSTANTS.MachinesKnown
        _distros = CONSTANTS.DistrosKnown
        _builtin_classes = ['class-native', 'class-target', 'class-nativesdk', 'class-cross']
        _operations = ['append', 'prepend', 'remove']
        for i in items:
            subs = [(x, stash.ExpandTerm(_file, x)) for x in i.SubItems]
            for subitem in subs:
                sub, expanded = subitem
                if (expanded in _builtin_classes) or (sub in _builtin_classes):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if (expanded in _packages) or (sub in _packages):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if (expanded in _operations) or (sub in _operations):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if (expanded in _distros) or (sub in _distros):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if (expanded in _named_res) or (sub in _named_res):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if (expanded in _machines) or (sub in _machines):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if _comp and (RegexRpl.match(_comp, expanded) or RegexRpl.match(_comp, sub)):
                    continue  # pragma: nocover_3.9 - coverage looks buggy on 3.9
                if expanded.startswith('task-'):
                    continue
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(a=i.VarName, b=sub))
        return res
