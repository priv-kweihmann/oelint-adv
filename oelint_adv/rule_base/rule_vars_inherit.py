from typing import List, Tuple

from oelint_parser.cls_item import Inherit
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarInherit(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.inherit',
                         severity='warning',
                         message='<FOO>',
                         appendix=['inherit', 'inherit_defer'],
                         valid_from_release='scarthgap')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Inherit] = stash.GetItemsFor(filename=_file, classifier=Inherit.CLASSIFIER)
        for i in items:
            if '${' not in i.RealRaw and i.Statement == 'inherit_defer':
                if any(x in i.get_items() for x in ['native', 'nativesdk', 'cross']):
                    continue
                res += self.finding(i.Origin, i.InFileLine,
                                    'inherit_defer should only be used if there is a variable involved',
                                    appendix='inherit')
            if '${' in i.RealRaw and i.Statement == 'inherit':
                res += self.finding(i.Origin, i.InFileLine,
                                    'Variable detected in inherit statement. Use inherit_defer instead',
                                    appendix='inherit_defer')
        return res
