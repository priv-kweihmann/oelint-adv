import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintRequireNotFound(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.file.requirenotfound'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'require oelint_adv_test.inc',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.requirenotfound'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'require oelint_adv_test.inc',
                                     'oelint_adv_test.inc':
                                     'VAR = "a"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
