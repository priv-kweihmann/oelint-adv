import pytest
from base import TestBaseClass


class TestClassOelintVarsBugtrackerIsUrl(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.bugtrackerisurl'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            BUGTRACKER = "what_/the/f"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            BUGTRACKER = "what_/the/f"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.bugtrackerisurl'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            BUGTRACKER = "https://foo.com"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
