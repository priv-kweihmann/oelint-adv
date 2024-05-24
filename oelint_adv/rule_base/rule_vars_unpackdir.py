from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarRootfsPostprocessCommand(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.unpackdir',
                         severity='error',
                         valid_from_release='styhead',
                         message='Use ${UNPACKDIR} instead of ${WORKDIR}')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue=['S', 'B'])
        for i in items:
            if '${WORKDIR}' in i.VarValueStripped:
                res += self.finding(i.Origin, i.InFileLine)
        return res
