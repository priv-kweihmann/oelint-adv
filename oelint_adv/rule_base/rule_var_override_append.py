from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarOverrideAppend(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.overrideappend',
                         severity='warning',
                         message='This creates an empty scope which is then appended. It should be {op}:{_class} instead')
        self.pkgspecific = [
            'ALLOW_EMPTY',
            'ALTERNATIVE',
            'CONFFILES',
            'DEBIAN_NOAUTONAME',
            'DEBIANNAME',
            'DEPENDS',
            'DESCRIPTION',
            'FILES',
            'GROUPADD_PARAM',
            'INITSCRIPT_NAME',
            'INITSCRIPT_PARAMS',
            'INSANE_SKIP',
            'LICENSE',
            'PKG',
            'pkg_postinst',
            'pkg_postinst_ontarget',
            'pkg_postrm',
            'pkg_preinst',
            'pkg_prerm',
            'PRIVATE_LIBS',
            'RCONFLICTS',
            'RDEPENDS',
            'RPROVIDES',
            'RRECOMMENDS',
            'RREPLACES',
            'RSUGGESTS',
            'SECTION',
            'SKIP_FILEDEPS',
            'sstate',
            'SUMMARY',
            'SYSTEMD_AUTO_ENABLE',
            'SYSTEMD_SERVICE',
            'USERADD_PARAM',
        ]

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR)

        _store = set()

        for i in sorted(items, key=lambda key: key.Line):
            _items = [x for x in i.SubItems if x]
            if i.VarName in self.pkgspecific:
                _items = _items[1:]
            _scope = [x for x in _items if x not in ['append', 'prepend']]
            _op = [x for x in _items if x in ['append', 'prepend']]
            if not _scope or not _items:
                continue  # pragma: no cover
            _scope_key = i.VarName + ':' + '-'.join(_scope)
            if _op:
                if _items[0] not in _op and _scope_key not in _store:
                    res += self.finding(i.Origin, i.InFileLine,
                                        override_msg=self.Msg.format(op=_op[0], _class=':'.join(_scope)))
            _store.add(_scope_key)
        return res
