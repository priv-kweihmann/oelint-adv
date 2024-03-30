import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsDescriptionTooBrief(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.descriptiontoobrief'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SUMMARY = "ABC"
                                     DESCRIPTION = "AB"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SUMMARY = "ABC"
                                     DESCRIPTION = "A"
                                     DESCRIPTION:append = "B"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.descriptiontoobrief'])
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
                                     DESCRIPTION:append = "D"
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
