import pytest
from base import TestBaseClass


class TestClassOelintVarsNotNeededSpace(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.notneededspace'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            VAR = " a"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            VAR += " a"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.notneededspace'])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            VAR = " a"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            VAR += " a"
            '''
            },
        ],
    )
    def test_fix(self, input, id):
        self.fix_and_check(self._create_args_fix(input), id)

    @pytest.mark.parametrize('id', ['oelint.vars.notneededspace'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            VAR = "a"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            VAR += "a"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            VAR_append = " a"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
