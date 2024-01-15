from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.parser import INLINE_BLOCK
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class VarDuplicates(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.duplicate',
                         severity='warning',
                         message='<FOO>')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for c in ['DEPENDS', 'RDEPENDS']:
            items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                      attribute=Variable.ATTR_VAR, attributeValue=c)
            _items = {}
            for i in items:
                for x in [y for y in i.get_items(versioned=True) if y]:
                    machine_mods = i.SubItems
                    machine_mods_cleaned = '_'.join(
                        sorted([x for x in machine_mods if x not in ['append', 'prepend', 'remove']]))
                    m = RegexRpl.match('.*(?P<dyn>/dynamic-layers/.*?/).*', i.Origin)
                    if m:
                        machine_mods_cleaned += f'_{m.group("dyn")}'
                    if machine_mods_cleaned not in _items:
                        _items[machine_mods_cleaned] = []
                    _operations = i.AppendOperation()
                    if x in _items[machine_mods_cleaned]:
                        if x == INLINE_BLOCK:
                            continue
                        if not any(x in ['append', 'prepend', ' += ', ' =+ '] for x in _operations):
                            _items[machine_mods_cleaned] = [x]
                        else:
                            res += self.finding(i.Origin, i.InFileLine,
                                                'Item \'{x}\' was added multiple times to {c}'.format(x=x, c=c))
                    else:
                        if any(x in ['append', 'prepend', ' += ', ' =+ '] for x in _operations):
                            _items[machine_mods_cleaned].append(x)
                        elif 'remove' in _operations:
                            if x in _items[machine_mods_cleaned]:
                                _items[machine_mods_cleaned].remove(x)  # pragma: no cover
                        else:
                            _items[machine_mods_cleaned] = [x]
        return res
