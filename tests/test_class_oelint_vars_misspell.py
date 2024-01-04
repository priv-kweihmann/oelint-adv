import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsMispell(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.mispell'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'DPENDS += "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILS = "foo"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.mispell'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS_${PN} = "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'PACKAGECONFIG[foo] = "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'GOPATH = "abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     PACKAGECONFIG_A = "a"
                                     PACKAGECONFIG_B = "c"
                                     do_configure() {
                                         ./configure ${PACKAGECONFIG_A}
                                     }
                                     python do_foo() {
                                         d.getVar("PACKAGECONFIG_B")
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     PACKAGES += "${PN}-foo"
                                     INITSCRIPT_PARAMS_${PN}-foo = "bar"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FOO:qemux86 = "1"

                                     SRC_URI = "git://github.com/znc/znc.git;name=znc;branch=master;protocol=https \\
                                                git://github.com/jimloco/Csocket.git;destsuffix=git/third_party/Csocket;name=Csocket;branch=master;protocol=https"
                                     SRCREV_znc = "bf253640d33d03331310778e001fb6f5aba2989e"
                                     SRCREV_Csocket = "e8d9e0bb248c521c2c7fa01e1c6a116d929c41b4"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
