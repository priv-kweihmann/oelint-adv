import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass


class TestClassOelintVarsMultilineIdent(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.multilineident'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "\\
                a \\
            b \\
            "
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
    
    @pytest.mark.parametrize('id', ['oelint.vars.multilineident'])
    @pytest.mark.parametrize('occurrence', [2])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "a \\
            b \\
                "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            D = "a \\
            e \\
                "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A = "\\
            a \\
            b \\
            "
            '''
            },
        ],
    )
    def test_bad_two(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.multilineident'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "\\
                 a \\
                 b \\
                 e \\
            "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A = "\\
                a \\
                b \\
                e \\
            "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A = "\\
            "
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
