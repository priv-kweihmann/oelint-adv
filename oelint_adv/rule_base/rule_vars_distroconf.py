import fnmatch
from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule, Classification


class VarsDistroConf(Rule):
    def __init__(self) -> None:
        self.needles = [
            'MACHINE',
            'MACHINE_ARCH',
            'MACHINE_ESSENTIAL_EXTRA_RDEPENDS',
            'MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS',
            'MACHINE_EXTRA_RRECOMMENDS',
            'MACHINE_FEATURES',
            'MACHINE_FEATURES_BACKFILL',
            'MACHINE_FEATURES_BACKFILL_CONSIDERED',
            'IMAGE_INSTALL',
            'MACHINEOVERRIDES',
        ]

        super().__init__(id='oelint.vars.distroconf',
                         severity='warning',
                         run_on=[Classification.DISTROCONF],
                         message='{var} should not be set as part of a distro configuration',
                         appendix=self.needles)

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR)

        for i in items:
            if not fnmatch.fnmatch(i.Origin, '*/distro/*.conf'):
                continue   # pragma: no cover
            if i.VarName in self.needles:
                res += self.finding(_file, i.InFileLine,
                                    self.Msg.format(var=i.VarName), appendix=i.VarName)
        return res
