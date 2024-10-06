import os
from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarOverride(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.override',
                         severity='error',
                         message='<FOO>')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _all: List[Variable] = list(x for x in stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER))  # noqa: C400
        for v in {x.VarName for x in _all}:
            items = [x for x in _all if x.VarName == v and x.IsImmediateModify()]
            items = sorted(items, key=lambda x: x.Line, reverse=False)
            for sub in [x.SubItem for x in items]:
                # Get all entries but not the only that do immediate expansion,
                # as these will be handled during parse time
                # and apply to different rules
                _items = [x for x in items if x.SubItem == sub and not x.IsAppend() and x.VarOp.strip() not in [
                    ':=', '?=', '??=']]
                if len(_items) > 1:
                    _files = {os.path.basename(x.Origin) for x in _items}
                    res += self.finding(_items[0].Origin, _items[0].InFileLine,
                                        'Variable \'{a}\' is set by \'{b}\''.format(
                                        a=v, b=','.join(_files)))
        return res
