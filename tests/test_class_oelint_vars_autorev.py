import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsAutorev(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.autorev'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRCREV = "${AUTOREV}"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.autorev'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
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
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
