import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarAppendOp(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.appendop'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A ??= "1"
            A += "2"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            B += "B"
            B ?= "A"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            C ??= "1"
            C .= "2"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            D .= "2"
            D ?= "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            F ??= "1"
            F =+ "2"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            G =+ "B"
            G ?= "A"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            H ??= "1"
            H =. "2"
            '''
            },
                        {
            'oelint_adv_test.bb':
            '''
            I =. "2"
            I ?= "1"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.appendop'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A ??= "1"
            A_append = "2"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            B_append = "B"
            B ?= "A"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            C ??= "1"
            C_append = "2"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            D_append = "2"
            D ?= "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            F ??= "1"
            F_prepend = "2"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            G_prepend = "B"
            G ?= "A"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            H ??= "1"
            H_prepend = "2"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            I_prepend = "2"
            I ?= "1"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)