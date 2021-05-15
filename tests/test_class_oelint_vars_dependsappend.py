import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsDependsAppend(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.dependsappend'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS = "bar"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.dependsappend'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS += "foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS_prepend =  "baz "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS_append = " xyz"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS_remove = "abc"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)