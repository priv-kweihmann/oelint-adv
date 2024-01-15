from collections import OrderedDict
from typing import List, Tuple

from oelint_parser.cls_item import (
    Export,
    Function,
    FunctionExports,
    Item,
    PythonBlock,
    Variable,
)
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class VarsPathHardcode(Rule):
    def __init__(self) -> None:
        self._map = OrderedDict({
            '/usr/lib/systemd/user': '${systemd_user_unitdir}',
            '/lib/systemd/system': '${systemd_system_unitdir}',
            '/usr/share/doc': '${docdir}',
            '/usr/share/info': '${infodir}',
            '/usr/share/man': '${mandir}',
            '/usr/libexec': '${libexecdir}',
            '/lib/systemd': '${systemd_unitdir}',
            '/usr/lib': '${libdir}',
            '/usr/bin': '${bindir}',
            '/usr/share': '${datadir}',
            '/usr/include': '${includedir}',
            '/var': '${localstatedir}',
            '/lib': '${nonarch_base_libdir}',
            '/usr/sbin': '${sbindir}',
            '/srv': '${servicedir}',
            '/com': '${sharedstatedir}',
            '/etc': '${sysconfdir}',
        })
        super().__init__(id='oelint.vars.pathhardcode',
                         severity='warning',
                         message='<FOO>',
                         appendix=[v.strip('$').strip('{').strip('}') for v in self._map.values()])

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Item] = stash.GetItemsFor(filename=_file,
                                              classifier=[Variable.CLASSIFIER, Export.CLASSIFIER,
                                                          Function.CLASSIFIER, FunctionExports.CLASSIFIER,
                                                          PythonBlock.CLASSIFIER])

        for i in items:
            if isinstance(i, Variable) and i.VarName in ['SUMMARY', 'DESCRIPTION', 'HOMEPAGE', 'AUTHOR',
                                                         'BUGTRACKER', 'FILES', 'CVE_STATUS']:
                continue
            _matches = []
            for k, v in self._map.items():
                for pre in ['^', '\'', '"', ' ', r'\$\{D\}', '=']:
                    for ext in [' ', '/', '"', r'\*', '$']:
                        for line in i.get_items():
                            if line.strip().startswith('#'):
                                continue
                            _match = RegexRpl.search(pre + k + ext, line)
                            if _match and k not in _matches:
                                _cleanapp = v.strip('$').strip('{').strip('}')
                                res += self.finding(i.Origin, i.InFileLine,
                                                    '\'{a}\' should be used instead of \'{b}\''.format(a=v, b=k), appendix=_cleanapp)
                                _parts = [x for x in k.split('/') if x]
                                for x in range(1, len(_parts) + 1):
                                    _k = '/' + '/'.join(_parts[0:x])
                                    _matches.append(_k)
        return res
