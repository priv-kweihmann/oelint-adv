import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass


class TestClassOelintVarsSectionLowerCase(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.sectionlowercase'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SECTION = "That's an awesome section"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.sectionlowercase'])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SECTION = "That's an awesome section"
            '''
            },
        ],
    )
    def test_fix(self, input, id):
        self.fix_and_check(self._create_args_fix(input), id)

    @pytest.mark.parametrize('id', ['oelint.vars.sectionlowercase'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SECTION = "that's an awesome section"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
