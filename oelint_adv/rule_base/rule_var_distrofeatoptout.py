from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule, Classification


class VarDistroFeatureOptOut(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.distrofeatureoptout',
                         severity='warning',
                         message="'DISTRO_FEATURES_OPTED_OUT' should be used to remove DISTRO_FEATURES",
                         run_on=[Classification.DISTROCONF],
                         valid_from_release='wrynose')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='DISTRO_FEATURES')
        for i in items:
            if 'remove' not in i.SubItems:
                continue
            res += self.finding(i.Origin, i.InFileLine)
        return res
