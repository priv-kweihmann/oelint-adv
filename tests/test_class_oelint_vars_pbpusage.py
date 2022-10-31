import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsPBPUsage(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.pbpusage'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "file://${P}.patch"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "git://${P}.com/${P}.git"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "https://foo.org/${P}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'S = "${WORDKIR}/${P}"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.pbpusage'])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "file://${P}.patch"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "git://${P}.com/${P}.git"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "https://foo.org/${P}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'S = "${WORDKIR}/${P}"',
                                 },
                             ],
                             )
    def test_fix(self, input_, id_):
        self.fix_and_check(self._create_args_fix(input_), id_)

    @pytest.mark.parametrize('id_', ['oelint.vars.pbpusage'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "file://${BP}.patch"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "git://${BP}.com/${BP}.git"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "https://foo.org/${BP}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'S = "${WORDKIR}/${BP}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRCREV_${P} = "01234567890abcdef"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
