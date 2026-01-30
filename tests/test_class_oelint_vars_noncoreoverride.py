import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsNonCoreOverride(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.noncoreoverride'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bbappend':
                                     '''
                                     do_install:append() {
                                        echo "foo"
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     '''
                                     PACKAGE_BEFORE_PN:append = " ${PN}-foo"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.noncoreoverride'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bbappend':
                                     '''
                                     do_install:append:my-distro() {
                                        echo "foo"
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     '''
                                     PACKAGE_BEFORE_PN:append:my-machine = " ${PN}-foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install:append() {
                                        echo "foo"
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     PACKAGE_BEFORE_PN:append = " ${PN}-foo"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
