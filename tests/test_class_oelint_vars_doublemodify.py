import pytest
from .base import TestBaseClass


class TestClassOelintVarsDoubleModify(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.doublemodify'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A_append_prepend_remove += "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A_append_prepend += "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A_append += "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A_prepend_remove += "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A_append_remove += "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A_remove += "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A_append_prepend_remove = " 1 "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A_append_remove = " 1 "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A_prepend_remove = " 1 "
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.doublemodify'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A_append = " a"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A_prepend = "a "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A_remove = "a"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A += "a"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A =+ "a"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
