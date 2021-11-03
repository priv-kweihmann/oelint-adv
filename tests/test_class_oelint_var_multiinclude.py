import pytest
from base import TestBaseClass


class TestClassOelintVarMultiInclude(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.var.multiinclude'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            include abc.inc
            B = "2"
            include abc.inc
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            require abc.inc
            B = "2"
            include abc.inc
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.var.multiinclude'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            include abc.inc
            B = "2"
            include abc2.inc
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
