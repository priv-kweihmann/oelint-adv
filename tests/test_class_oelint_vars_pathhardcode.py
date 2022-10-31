import os

import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsPathHardcode(TestBaseClass):

    def __generate_sample_code(self, var):
        return '''
            VAR = "{var}"
            '''.format(var=var)

    @pytest.mark.parametrize('id_', ['oelint.vars.pathhardcode'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('pair', [
        ('${systemd_user_unitdir}', '/usr/lib/systemd/user'),
        ('${systemd_system_unitdir}', '/lib/systemd/system'),
        ('${docdir}', '/usr/share/doc'),
        ('${infodir}', '/usr/share/info'),
        ('${mandir}', '/usr/share/man'),
        ('${libexecdir}', '/usr/libexec'),
        ('${systemd_unitdir}', '/lib/systemd'),
        ('${libdir}', '/usr/lib'),
        ('${bindir}', '/usr/bin'),
        ('${datadir}', '/usr/share'),
        ('${includedir}', '/usr/include'),
        ('${localstatedir}', '/var'),
        ('${nonarch_base_libdir}', '/lib'),
        ('${sbindir}', '/usr/sbin'),
        ('${servicedir}', '/srv'),
        ('${sharedstatedir}', '/com'),
        ('${sysconfdir}', '/etc'),
    ])
    def test_bad(self, id_, occurrence, pair):
        id_ += '.{var}'.format(var=pair[0].strip('${}'))  # noqa: P103 - false positive
        for variation in [pair[1],
                          pair[1] + '/',
                          os.path.join(pair[1], 'fooooo/ggsg'),
                          os.path.join(pair[1], '*'),
                          os.path.join('${D}', pair[1])]:
            input_ = {
                'oelint_adv_test.bb': self.__generate_sample_code(variation),
            }
            self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.pathhardcode'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('pair', [
        ('${systemd_user_unitdir}', '/usr/lib/systemd/user'),
        ('${systemd_system_unitdir}', '/lib/systemd/system'),
        ('${docdir}', '/usr/share/doc'),
        ('${infodir}', '/usr/share/info'),
        ('${mandir}', '/usr/share/man'),
        ('${libexecdir}', '/usr/libexec'),
        ('${systemd_unitdir}', '/lib/systemd'),
        ('${libdir}', '/usr/lib'),
        ('${bindir}', '/usr/bin'),
        ('${datadir}', '/usr/share'),
        ('${includedir}', '/usr/include'),
        ('${localstatedir}', '/var'),
        ('${nonarch_base_libdir}', '/lib'),
        ('${nonarch_libdir}', '/usr/lib'),
        ('${oldincludedir}', '/usr/include'),
        ('${sbindir}', '/usr/sbin'),
        ('${servicedir}', '/srv'),
        ('${sharedstatedir}', '/com'),
        ('${sysconfdir}', '/etc'),
    ])
    def test_good(self, id_, occurrence, pair):
        id_ += '.{var}'.format(var=pair[0].strip('${}'))  # noqa: P103 - false positive
        for variation in [pair[0],
                          pair[0] + '/',
                          os.path.join(pair[0], 'fooooo/ggsg'),
                          os.path.join(pair[0], '*'),
                          os.path.join('${D}', pair[0])]:
            input_ = {
                'oelint_adv_test.bb': self.__generate_sample_code(variation),
            }
            self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.pathhardcode'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES_${PN} += "/usr/lib/totally.valid.file"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES_${PN} += "/usr/bin/totally.valid.file"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         #To remove the default files from /etc/somefolder
                                         rm -f ${D}${sysconfdir}/somefolder/*
                                         install -m 0644 ${S}/usr/lib/* ${D}${libdir}
                                         install -m 0644 ${WORKDIR}/usr/bin ${D}${bindir}
                                         echo "foo" | sed "s#/usr/bin/python#/usr/bin/env python#g" > ${D}${bindir}/foo
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good_pattern(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
