import re
from collections import OrderedDict

from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Comment
from oelint_parser.cls_item import Variable


class VarsPathHardcode(Rule):
    def __init__(self):
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

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)

        for i in items:
            if isinstance(i, Variable) and i.VarName in ['SUMMARY', 'DESCRIPTION', 'HOMEPAGE', 'AUTHOR', 'BUGTRACKER', 'FILES']:
                continue
            if isinstance(i, Comment):
                continue
            _matches = []
            for k, v in self._map.items():
                for pre in ['^', '\'', '"', ' ', r'\$\{D\}', '=']:
                    for ext in [' ', '/', '"', r'\*', '$']:
                        for line in i.get_items():
                            if line.strip().startswith('#'):
                                continue
                            _match = re.search(pre + k + ext, line)
                            if _match and k not in _matches:
                                _cleanapp = v.strip('$').strip('{').strip('}')
                                res += self.finding(i.Origin, i.InFileLine,
                                                    '\'{a}\' should be used instead of \'{b}\''.format(a=v, b=k), appendix=_cleanapp)
                                _parts = [x for x in k.split('/') if x]
                                for x in range(1, len(_parts) + 1):
                                    _k = '/' + '/'.join(_parts[0:x])
                                    _matches.append(_k)
        return res
