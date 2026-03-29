import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsPKGSpecific(TestBaseClass):

    def __generate_sample_code(self, var):
        return '''
            {var} = "foo"
            '''.format(var=var)

    @pytest.mark.parametrize('id_', ['oelint.vars.pkgspecific'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'RDEPENDS',
        'RRECOMMENDS',
        'RSUGGESTS',
        'RCONFLICTS',
        'RPROVIDES',
        'RREPLACES',
        'FILES',
        'pkg_preinst',
        'pkg_postinst',
        'pkg_prerm',
        'pkg_postrm',
        'ALLOW_EMPTY',
    ])
    def test_bad(self, id_, occurrence, var):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(var),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.pkgspecific'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'RDEPENDS',
        'RRECOMMENDS',
        'RSUGGESTS',
        'RCONFLICTS',
        'RPROVIDES',
        'RREPLACES',
        'FILES',
        'pkg_preinst',
        'pkg_postinst',
        'pkg_prerm',
        'pkg_postrm',
        'ALLOW_EMPTY',
    ])
    def test_bad_append_with_bb(self, id_, occurrence, var):
        input_ = {
            'oelint-adv-test_1.0.bb': 'VAR = "FOO"',
            'oelint-adv-test_1.0.bbappend': self.__generate_sample_code(var),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)
        input_reversed_ = {k: input_[k] for k in reversed(input_)}
        self.check_for_id(self._create_args(input_reversed_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.pkgspecific'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'RDEPENDS_${PN}',
        'RRECOMMENDS_${PN}',
        'RSUGGESTS_${PN}',
        'RCONFLICTS_${PN}',
        'RPROVIDES_${PN}',
        'RREPLACES_${PN}',
        'FILES_${PN}',
        'pkg_preinst_${PN}',
        'pkg_postinst_${PN}',
        'pkg_prerm_${PN}',
        'pkg_postrm_${PN}',
        'ALLOW_EMPTY_${PN}',
    ])
    def test_good(self, id_, occurrence, var):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(var),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.pkgspecific'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'RDEPENDS_foo',
        'RRECOMMENDS_foo',
        'RSUGGESTS_foo',
        'RCONFLICTS_foo',
        'RPROVIDES_foo',
        'RREPLACES_foo',
        'FILES_foo',
        'pkg_preinst_foo',
        'pkg_postinst_foo',
        'pkg_prerm_foo',
        'pkg_postrm_foo',
        'ALLOW_EMPTY_foo',
    ])
    def test_good_bbappend(self, id_, occurrence, var):
        input_ = {
            'oelint_adv_test_%.bbappend': self.__generate_sample_code(var),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', [
        'oelint.vars.pkgspecific.RDEPENDS',
        'oelint.vars.pkgspecific.RRECOMMENDS',
        'oelint.vars.pkgspecific.RSUGGESTS',
        'oelint.vars.pkgspecific.RCONFLICTS',
        'oelint.vars.pkgspecific.RPROVIDES',
        'oelint.vars.pkgspecific.RREPLACES',
        'oelint.vars.pkgspecific.FILES',
        'oelint.vars.pkgspecific.pkg_preinst',
        'oelint.vars.pkgspecific.pkg_postinst',
        'oelint.vars.pkgspecific.pkg_prerm',
        'oelint.vars.pkgspecific.pkg_postrm',
        'oelint.vars.pkgspecific.ALLOW_EMPTY',
    ])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     PACKAGES += "abc-foo"
                                     RDEPENDS_abc-foo += "bar"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     PACKAGES_DYNAMIC = "^${PN}-lib.* ^foo-"
                                     RDEPENDS:${PN}-libfoo += "baz"
                                     RSUGGESTS:oelint-libbar += "baz"
                                     FILES:foo-bar += "baz"
                                     ''',
                                 },
                             ],
                             )
    def test_good_custom_pkg(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
