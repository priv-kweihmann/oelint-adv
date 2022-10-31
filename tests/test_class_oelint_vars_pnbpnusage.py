import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsPNBPNUsage(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.pnbpnusage'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "file://${PN}.patch"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "git://${PN}.com/${PN}.git"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "https://foo.org/${PN}"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.pnbpnusage'])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "file://${PN}.patch"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "git://${PN}.com/${PN}.git"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "https://foo.org/${PN}"',
                                 },
                             ],
                             )
    def test_fix(self, input_, id_):
        self.fix_and_check(self._create_args_fix(input_), id_)

    @pytest.mark.parametrize('id_', ['oelint.vars.pnbpnusage'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "file://${BPN}.patch"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "git://${BPN}.com/${BPN}.git"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "https://foo.org/${BPN}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'S = "${WORDKIR}/${BPN}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "git://foo.org/baz.git;name=${PN}-super"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "git://foo.org/${BPN}.git;name=${PN}-ultra"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
