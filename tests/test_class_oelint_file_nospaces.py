import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintFileNoSpaces(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.file.nospaces'])
    @pytest.mark.parametrize('occurance', [1])
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
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)
