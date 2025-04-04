import fnmatch
from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule, Classification


class VarsMachineConf(Rule):
    def __init__(self) -> None:
        self.needles = [
            'DISTROOVERRIDES',
            'DISTRO_EXTRA_RDEPENDS',
            'DISTRO_EXTRA_RRECOMMENDS',
            'DISTRO_FEATURES',
            'DISTRO_FEATURES_BACKFILL',
            'DISTRO_FEATURES_BACKFILL_CONSIDERED',
            'DISTRO_FEATURES_DEFAULT',
            'IMAGE_INSTALL',
        ]

        super().__init__(id='oelint.vars.machineconf',
                         severity='warning',
                         message='{var} should not be set as part of a machine configuration',
                         run_on=[Classification.MACHINECONF],
                         appendix=self.needles)

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR)

        for i in items:
            if not fnmatch.fnmatch(i.Origin, '*/machine/*.conf'):
                continue  # pragma: no cover
            if i.VarName in self.needles:
                res += self.finding(_file, i.InFileLine,
                                    self.Msg.format(var=i.VarName), appendix=i.VarName)
        return res
