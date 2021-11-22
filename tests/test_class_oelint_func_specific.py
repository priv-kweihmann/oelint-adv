import pytest

from .base import TestBaseClass


class TestClassOelintFuncSpecific(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.func.specific'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     do_install_append_fooarch() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     do_configure_bararch() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     COMPATIBLE_MACHINE = "xyz"
                                     do_install_fooarch() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     COMPATIBLE_MACHINE = "xyz"
                                     do_configure_append_bararch() {
                                         abc
                                     }
                                     ''',
                                 },

                             ],
                             )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.func.specific'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     do_install_ptest () {
                                         cp -r ${B}/testsuite ${D}${PTEST_PATH}/
                                         cp ${B}/.config      ${D}${PTEST_PATH}/
                                         ln -s /bin/busybox   ${D}${PTEST_PATH}/busybox
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     do_install_qemuall () {
                                         cp -r ${B}/testsuite ${D}${PTEST_PATH}/
                                         cp ${B}/.config      ${D}${PTEST_PATH}/
                                         ln -s /bin/busybox   ${D}${PTEST_PATH}/busybox
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     COMPATIBLE_MACHINE = "foo"
                                     do_install_append_fooarch() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     COMPATIBLE_MACHINE += "|bar"
                                     do_configure_append_bararch() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     pkg_preinst_${PN} () {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     do_configure:poky() {
                                         abc
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
