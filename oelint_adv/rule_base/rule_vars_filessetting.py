from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarUnneededFilesSetting(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.filessetting',
                         severity='warning',
                         message='Check for improvable FILES settings',
                         appendix=['hidden', 'double'])

    def __find_match_from_stash(self,
                                _files: List[Variable],
                                variable_: str,
                                needle: str,
                                msg: str,
                                appendix: str,
                                onappendonly: bool = False) -> List[Tuple[str, int, str]]:
        res = []
        for i in _files:
            if variable_ in i.SubItems and 'remove' not in i.SubItems and needle in i.VarValue:  # pragma: no cover
                if (onappendonly and i.IsAppend()) or (not onappendonly):
                    res += self.finding(i.Origin, i.InFileLine,
                                        override_msg=msg, appendix=appendix)
        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _expanded = stash.ExpandVar(filename=_file, attribute=Variable.ATTR_VAR)
        _all_files = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                       attribute=Variable.ATTR_VAR, attributeValue='FILES')
        if not any(_all_files):
            return res
        override_delimiter = _all_files[-1].OverrideDelimiter
        _seenpath = {}
        for p in _expanded['PACKAGES']:
            _files = 'FILES{o}{a}'.format(o=override_delimiter, a=p)
            _convfiles = _files.replace(_expanded['PN'][0], '${PN}')
            if _files in _expanded:
                _pattern = _expanded[_files]
                for _p in _pattern:
                    # double setting in FILES
                    # try to find with both unexpanded and expanded values
                    if len([x for x in _pattern if x == _p]) > 1:
                        res += self.__find_match_from_stash(_all_files, p.replace(_expanded['PN'][0], '${PN}'), _p,
                                                            '{a} is already set by default or in this recipe'.format(a=_p), 'double', True)
                        res += self.__find_match_from_stash(_all_files, p, _p,
                                                            '{a} is already set by default or in this recipe'.format(a=_p), 'double', True)
                    # useless as hidden by previous package
                    if _p in _seenpath.keys() and _seenpath[_p] != _convfiles:
                        # try to find with both unexpanded and expanded values
                        res += self.__find_match_from_stash(_all_files, p.replace(_expanded['PN'][0], '${PN}'), _p,
                                                            '{a} is already covered by {b}'.format(a=_p, b=_seenpath[_p]),
                                                            'hidden')
                        res += self.__find_match_from_stash(_all_files, p, _p,
                                                            '{a} is already covered by {b}'.format(a=_p, b=_seenpath[_p]),
                                                            'hidden')
                    _seenpath[_p] = _convfiles
        return res
