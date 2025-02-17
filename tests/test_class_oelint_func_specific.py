import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintFuncSpecific(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.func.specific'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     do_install:append:fooarch() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     do_configure:bararch() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     COMPATIBLE_MACHINE = "xyz"
                                     do_install:fooarch() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     COMPATIBLE_MACHINE = "xyz"
                                     do_configure:append:bararch() {
                                         abc
                                     }
                                     ''',
                                 },

                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.func.specific'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
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
                                     COMPATIBLE_MACHINE = "xyz"
                                     do_install_append_bararch() {
                                         abc
                                     }
                                     ''',
                                 },

                             ],
                             )
    def test_bad_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.func.specific'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     do_install:ptest () {
                                         cp -r ${B}/testsuite ${D}${PTEST_PATH}/
                                         cp ${B}/.config      ${D}${PTEST_PATH}/
                                         ln -s /bin/busybox   ${D}${PTEST_PATH}/busybox
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     do_install:qemuall () {
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
                                     do_install:append:fooarch() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     COMPATIBLE_MACHINE += "|bar"
                                     do_configure:append:bararch() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     pkg_preinst:${PN} () {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     do_configure:nodistro() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     A = "nodistro"
                                     do_configure:${A} () {
                                         abc
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.func.specific'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
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
                             ],
                             )
    def test_good_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)
