import pytest

from .base import TestBaseClass


class TestClassOelintVarsSummaryLineBreaks(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.summarylinebreaks'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SUMMARY = "a\\n"',
                                 },
                             ],
                             )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.summarylinebreaks'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SUMMARY = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SUMMARY = "a \\
                                         b"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
