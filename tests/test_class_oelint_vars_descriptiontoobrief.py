import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsDescriptionTooBrief(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.descriptiontoobrief'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SUMMARY = "ABC"
            DESCRIPTION = "AB"
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.descriptiontoobrief'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SUMMARY = "ABC"
            DESCRIPTION = "ABCD"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SUMMARY = "ABC"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DESCRIPTION = "ABCD"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)