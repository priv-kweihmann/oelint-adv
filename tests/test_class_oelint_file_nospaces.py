import pytest
from .base import TestBaseClass


class TestClassOelintFileNoSpaces(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.file.nospaces'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
