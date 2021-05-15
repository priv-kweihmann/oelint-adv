import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintTaskCustomOrder(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.task.customorder'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            addtask do_compile after do_configure
            addtask do_configure after do_compile
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_foo() {
                :
            }
            addtask do_compile after do_configure
            addtask do_foo before do_configure after do_compile
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.customorder'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            addtask do_compile after do_foo
            addtask do_configure after do_compile
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)