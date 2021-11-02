import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass


class TestClassOelintVarsInsaneSkip(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.insaneskip'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            INSANE_SKIP_${PN} = "a"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            INSANE_SKIP_bla = "a"
            '''
            },
                        {
            'oelint_adv_test.bb':
            '''
            INSANE_SKIP_bla_class-native = "a"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.insaneskip'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            VAR += "ffjjj"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
