from typing import List, Tuple

from oelint_parser.cls_item import Variable, Inherit
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarSRCURIAppend(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.srcuriappend',
                         severity='error',
                         message='<FOO>')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        inherits = stash.GetItemsFor(filename=_file, classifier=Inherit.CLASSIFIER)
        if not inherits:
            return res

        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')
        for item in items:
            if item.VarOp.strip() in ['+=']:
                override_delimiter = item.OverrideDelimiter
                res += self.finding(item.Origin, item.InFileLine,
                                    'Use SRC_URI{od}append otherwise this will override weak defaults by inherit'.format(
                                        od=override_delimiter))
        return res
