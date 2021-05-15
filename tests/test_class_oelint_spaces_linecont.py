import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintSpacesLineCont(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.spaces.linecont'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            ABC = "1 \\ 
                "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS += "\\
               a \\
               b \\ 
               c \\
            "
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.spaces.linecont'])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            ABC = "1 \\ 
                "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS += "\\
               a \\
               b \\ 
               c \\
            "
            '''
            }
        ],
    )
    def test_fix(self, input, id):
        self.fix_and_check(self._create_args_fix(input), id)

    @pytest.mark.parametrize('id', ['oelint.spaces.linecont'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS += "\\
               a \\
               b \\
               c \\
            "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            ABC = "1 \\
                "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            # this is just a comment \\ 
            # so don't mind that
            '''
            }
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)