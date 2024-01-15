from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarFilesOverride(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.filesoverride',
                         severity='warning',
                         message='\'{a}\' should not be overriden')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue='FILES')
        for i in items:
            if not i.AppendOperation():
                res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format(a=i.VarName))
        return res
