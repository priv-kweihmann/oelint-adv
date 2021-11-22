import pytest

from .base import TestBaseClass


class TestClassOelintVarsAutorev(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.autorev'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRCREV = "${AUTOREV}"',
                                 },
                             ],
                             )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.autorev'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRCREV = "abcdefgehijk"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRCREV = "${SOMEOTHERVAR}"',
                                 },
                             ],
                             )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
