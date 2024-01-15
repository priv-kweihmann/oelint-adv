from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarRootfsPostprocessCommand(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.rootfspostcmd',
                         severity='warning',
                         message='ROOTFS_POSTPROCESS_COMMAND should not have trailing blanks')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='ROOTFS_POSTPROCESS_COMMAND')
        for i in items:
            _chunks = i.VarValueStripped.split(';')
            if any(True for x in _chunks if x.strip() and x.endswith(' ')):
                res += self.finding(i.Origin, i.InFileLine)
        return res
