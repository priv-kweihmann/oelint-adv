import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsDUsagePkgFunc(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.dusageinpkgfuncs'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_preinst:${PN} () {
                                         if [ -n "${D}" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_postinst:${PN} () {
                                         if [ -n "${D}" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_prerm:${PN} () {
                                         if [ -n "${D}" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_postrm:${PN} () {
                                         if [ -n "${D}" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.dusageinpkgfuncs'])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_preinst:${PN} () {
                                         if [ -n "${D}" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_postinst:${PN} () {
                                         if [ -n "${D}" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_prerm:${PN} () {
                                         if [ -n "${D}" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_postrm:${PN} () {
                                         if [ -n "${D}" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_fix(self, input_, id_):
        self.fix_and_check(self._create_args_fix(input_), id_)

    @pytest.mark.parametrize('id_', ['oelint.vars.dusageinpkgfuncs'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_preinst:${PN} () {
                                         if [ -n "$D" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_postinst:${PN} () {
                                         if [ -n "$D" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_prerm:${PN} () {
                                         if [ -n "$D" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_postrm:${PN} () {
                                         if [ -n "$D" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     pkg_postrm:${PN} () {
                                         if [ -n "${Z}" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install () {
                                         if [ -n "${D}" ]; then
                                             echo "Foo"
                                         fi
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
