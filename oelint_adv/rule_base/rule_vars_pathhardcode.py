from oelint_adv.cls_rule import Rule

from collections import OrderedDict


class VarsPathHardcode(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.pathhardcode",
                         severity="warning",
                         message="<FOO>")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        _map = OrderedDict({
            "/usr/lib/systemd/user": "${systemd_user_unitdir}",
            "/lib/systemd/system": "${systemd_system_unitdir}",
            "/usr/share/doc": "${docdir}",
            "/usr/share/info": "${infodir}",
            "/usr/share/man": "${mandir}",
            "/usr/libexec": "${libexecdir}",
            "/lib/systemd": "${systemd_unitdir}",
            "/usr/lib": "${libdir}",
            "/usr/bin": "${bindir}",
            "/usr/share": "${datadir}",
            "/usr/include": "${includedir}",
            "/var": "${localstatedir}",
            "/lib": "${nonarch_base_libdir}",
            "/usr/sbin": "${sbindir}",
            "/srv": "${servicedir}",
            "/com": "${sharedstatedir}",
            "/etc": "${sysconfdir}",
        })
        for i in items:
            _matches = []
            for k, v in _map.items():
                for ext in [" ", "/", "\""]:
                    if k + ext in i.Raw and k not in _matches:
                        res += self.finding(i.Origin, i.InFileLine,
                                            "'{}' should be used instead of '{}'".format(v, k))
                        _parts = [x for x in k.split("/") if x]
                        for x in range(0, len(_parts)):
                            _matches.append("/" + "/".join(_parts[0:x]))
        return res
