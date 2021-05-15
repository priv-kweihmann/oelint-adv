import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarImproperInherit(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.var.improperinherit'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            inherit abc/abc abc
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit def~AAAA
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit ghi>bbclass
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.var.improperinherit'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            inherit abc def
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit A0_a
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit update-rc.d
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit ${@magic_call(d)}
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            XORGBUILDCLASS ??= "autotools"
            inherit ${XORGBUILDCLASS} pkgconfig features_check
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)