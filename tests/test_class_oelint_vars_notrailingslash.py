import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsNoTrailingSlash(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.notrailingslash'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'S = "${WORDKIR}/foo/"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'D = "${WORDKIR}/foo/"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'T = "${WORDKIR}/foo/"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'B = "${WORDKIR}/foo/"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     BAR = "foo/"
                                     S = "${WORDKIR}/${BAR}"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.notrailingslash'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'S = "${WORDKIR}/foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'D = "${WORDKIR}/foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'T = "${WORDKIR}/foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'B = "${WORDKIR}/foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     BAR = "foo"
                                     S = "${WORDKIR}/${BAR}"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SOMEOTHERVAR = "foo/"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
