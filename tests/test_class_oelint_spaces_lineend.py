import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass


class TestClassOelintSpacesLineEnd(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.spaces.lineend'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            ABC = "1" 
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            # just a comment 
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.spaces.lineend'])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            ABC = "1" 
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            # just a comment 
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            ABC = "1" 
            ABC += "2" 
            '''
            }
        ],
    )
    def test_fix(self, input, id):
        self.fix_and_check(self._create_args_fix(input), id)

    @pytest.mark.parametrize('id', ['oelint.spaces.lineend'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            ABC = "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEF = "${@foo_magic_grill(d)}"
            '''
            }
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
