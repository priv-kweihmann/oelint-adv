import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintNewlineConsecutive(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.newline.consecutive'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "1"


            B = "1"
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.newline.consecutive'])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "1"


            B = "1"
            '''
            }
        ],
    )
    def test_fix(self, input, id):
        self.fix_and_check(self._create_args_fix(input), id)

    @pytest.mark.parametrize('id', ['oelint.newline.consecutive'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "1"

            B = "1"
            C = "1"

            D = "1"
            '''
            }
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)