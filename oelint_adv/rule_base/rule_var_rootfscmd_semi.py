from typing import List

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarRootfsPostprocessCommand(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.rootfspostcmdsemicolon',
                         severity='warning',
                         message='ROOTFS_POSTPROCESS_COMMAND is space separated. Please remove all ";"',
                         valid_from_release='blacksail')

    def check(self, _file: str, stash: Stash) -> List[Rule.Finding]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='ROOTFS_POSTPROCESS_COMMAND')
        for i in items:
            if ';' in i.VarValueStripped:
                res += self.finding(i.Origin, i.InFileLine)
        return res
