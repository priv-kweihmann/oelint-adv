import pytest
from base import TestBaseClass


class TestClassOelintFileIncludeNotFound(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.file.includenotfound'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            include oelint_adv_test.inc
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.file.includenotfound'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            include oelint_adv_test.inc
            '''
            ,
            'oelint_adv_test.inc':
            '''
            VAR = "a"
            '''
            }
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
