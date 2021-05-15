import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsNoTrailingSlash(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.notrailingslash'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            S = "${WORDKIR}/foo/"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            D = "${WORDKIR}/foo/"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            T = "${WORDKIR}/foo/"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            B = "${WORDKIR}/foo/"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            BAR = "foo/"
            S = "${WORDKIR}/${BAR}"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.notrailingslash'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
                        {
            'oelint_adv_test.bb':
            '''
            S = "${WORDKIR}/foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            D = "${WORDKIR}/foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            T = "${WORDKIR}/foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            B = "${WORDKIR}/foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            BAR = "foo"
            S = "${WORDKIR}/${BAR}"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SOMEOTHERVAR = "foo/"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)