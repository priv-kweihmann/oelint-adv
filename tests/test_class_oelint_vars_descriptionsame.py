import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsDescriptionSame(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.descriptionsame'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SUMMARY = "ABC"
                                     DESCRIPTION = "ABC"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SUMMARY = "ABC"
                                     DESCRIPTION = "A"
                                     DESCRIPTION:append = "BC"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.descriptionsame'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SUMMARY = "ABC"
                                     DESCRIPTION = "ABCD"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SUMMARY = "ABC"
                                     DESCRIPTION = "ABC"
                                     DESCRIPTION += "D"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SUMMARY = "ABC"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DESCRIPTION = "ABCD"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
