from typing import List, Tuple

from oelint_parser.cls_item import Variable, FlagAssignment
from oelint_parser.cls_stash import Stash
from oelint_parser.parser import INLINE_BLOCK

from oelint_adv.cls_rule import Rule


class VarSRCURIMutualExItems(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.srcurimutualex',
                         severity='error',
                         message="'SRCREV' and a checksum are defined for the same item - only one is applicable")

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _srcuri: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                    attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')
        _map = {}
        for item in _srcuri:
            for value in [x.strip("'") for x in item.get_items() if x and INLINE_BLOCK not in x]:
                components = stash.GetScrComponents(value)

                _map[components['options'].get('name', '')] = {
                    'type': components['scheme']}

        _srcrevs: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                     attribute=Variable.ATTR_VAR,
                                                     attributeValue=['SRCREV'] + [f'SRCREV_{k}' for k in _map.keys() if k])
        _flags: List[Variable] = stash.GetItemsFor(filename=_file, classifier=FlagAssignment.CLASSIFIER,
                                                   attribute=FlagAssignment.ATTR_NAME,
                                                   attributeValue='SRC_URI')

        for item in _srcrevs:
            needle = item.VarNameCompleteNoModifiers.split('_')[-1]
            if needle == 'SRCREV':
                needle = ''
            if needle in _map:
                _map[needle]['srcrev'] = item

        for item in _flags:
            if item.Flag.endswith('sum'):
                needle = item.Flag.split('.')[0]
                _sum = item.Flag.split('.')[-1]
                if needle.endswith('sum'):
                    needle = ''
                if needle in _map:
                    _map[needle][_sum] = item

        for _, v in _map.items():
            if 'srcrev' not in v:
                continue
            for sk, sv in v.items():
                if not sk.endswith('sum'):
                    continue
                res += self.finding(sv.Origin, sv.InFileLine)
        return res
