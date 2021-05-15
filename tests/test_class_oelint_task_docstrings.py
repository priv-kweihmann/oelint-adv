import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintTaskDocstrings(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.task.docstrings'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_foo() {
                :
            }
            addtask do_foo
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.docstrings'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_foo() {
                :
            }
            addtask do_foo
            do_foo[doc] = "Fooo!!!!"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_foo[doc] = "Fooo!!!!"
            do_foo() {
                :
            }
            addtask do_foo
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)