import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsBugtrackerIsUrl(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.bugtrackerisurl'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'BUGTRACKER = "what_/the/f"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'BUGTRACKER = "what_/the/f"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.bugtrackerisurl'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'BUGTRACKER = "https://foo.com"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
