import os
from difflib import SequenceMatcher
from typing import List, Tuple

from oelint_parser.cls_item import FlagAssignment, Function, Item, Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class VarMisspell(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.mispell',
                         severity='warning',
                         message='<FOO>',
                         appendix=['unknown'])
        try:
            self._minconfidence = float(os.environ.get('OELINT_MISSPELL_CONFIDENCE', 'not-a-float'))
        except ValueError:
            self._minconfidence = 0.8

        self._layername_extensions_on = [
            'BBFILE_PATTERN',
            'BBFILE_PRIORITY',
            'BBFILE_PATTERN_IGNORE_EMPTY',
            'LAYERDEPENDS',
            'LAYERRECOMMENDS',
            'LAYERSERIES_COMPAT',
            'LAYERVERSION',
        ]

    def get_best_match(self, item: str, _list: List[str]) -> str:
        _dict = sorted([(SequenceMatcher(None, item, k).ratio(), k)
                        for k in _list], key=lambda x: x[0], reverse=True)
        if _dict and _dict[0][0] >= self._minconfidence:
            return _dict[0][1]
        return ''

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []

        _all: List[Item] = stash.GetItemsFor(filename=_file)
        items: List[Item] = stash.Reduce(_all, filename=_file, classifier=[Variable.CLASSIFIER, FlagAssignment.CLASSIFIER])
        _extras = [f'SRCREV_{x}' for x in stash.GetValidNamedResources(_file)]
        _pkgs = [x for x in stash.GetValidPackageNames(_file, strippn=True) if x]
        _taskname = CONSTANTS.FunctionsKnown + [x.FuncName for x in _all if isinstance(x, Function)]
        _vars = CONSTANTS.VariablesKnown
        _bbfile_collections = stash.ExpandVar(_file, attribute=Variable.ATTR_VAR,
                                              attributeValue='BBFILE_COLLECTIONS').get('BBFILE_COLLECTIONS', [])
        for collection in _bbfile_collections:
            for var in self._layername_extensions_on:
                _vars.append(f'{var}_{collection}')

        for i in items:
            if isinstance(i, Variable):
                _cleanvarname = i.VarName
                if _cleanvarname.startswith('_'):
                    continue
                if _cleanvarname in _vars:
                    continue
                if _cleanvarname in _extras:
                    continue
                for pkg in _pkgs:
                    if _cleanvarname.endswith(pkg):
                        _cleanvarname = ''.join(_cleanvarname.rsplit(pkg, 1))  # pragma: no cover
            else:
                _cleanvarname = i.VarName
                if _cleanvarname.startswith('_'):
                    continue
                if _cleanvarname in _taskname:
                    continue
                if _cleanvarname in _vars:
                    continue
                if _cleanvarname in _extras:
                    continue
            _used = False
            for a in _all:
                if a == i:
                    continue
                if '${{{a}}}'.format(a=i.VarName) in a.Raw or 'getVar("{a}"'.format(a=i.VarName) in a.Raw:
                    _used = True
                    break
            if _used:
                continue
            _bestmatch = self.get_best_match(_cleanvarname, _vars)
            if _bestmatch:
                res += self.finding(i.Origin, i.InFileLine,
                                    '\'{a}\' is unknown, maybe you meant \'{b}\''.format(
                                        a=_cleanvarname, b=_bestmatch))
            else:
                res += self.finding(i.Origin, i.InFileLine,
                                    '\'{a}\' is unknown. Consider adding it via --constantmods'.format(a=_cleanvarname),
                                    appendix='unknown',
                                    severity_override='info')
        return res
