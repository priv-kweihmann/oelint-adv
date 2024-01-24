from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarsVirtualProvDep(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.virtual',
                         severity='error',
                         message='{var} can not contain virtual/ items')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue=['RDEPENDS', 'RPROVIDES'])

        for i in items:
            if any(x.startswith('virtual/') for x in i.get_items() if 'remove' not in i.SubItems):
                res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format(var=i.VarName))
        return res
