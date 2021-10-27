import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarOverride(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.var.override'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
            A = "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
            B = "0"
            A = "1"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.var.override'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
            A += "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
            A =+ "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
            A .= "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
            A =. "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
            A ?= "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
            A ??= "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILESEXTRAPATH_prepend := "a:"
            FILESEXTRAPATH_prepend := "b:"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILESEXTRAPATH_append := ":a"
            FILESEXTRAPATH_append := ":b"
            '''
            }
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
