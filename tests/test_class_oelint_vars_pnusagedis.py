import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsPNUsageDiscouraged(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.pnusagediscouraged'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'HOMEPAGE = "http://${PN}.com"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'BUGTRACKER = "http://${PN}.com"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SUMMARY = "http://${PN}.com"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DESCRIPTION = "http://${PN}.com"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.pnusagediscouraged'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'HOMEPAGE = "http://some.org.com"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'BUGTRACKER = "http://${FOO}.com"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SUMMARY = "ssas"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DESCRIPTION = "1"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
