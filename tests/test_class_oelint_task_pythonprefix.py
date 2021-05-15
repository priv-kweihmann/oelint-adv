import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintTaskPythonPrefix(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.task.pythonprefix'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_bar() {
                import os
                print("fooooooo!!!!")
            }
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.pythonprefix'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_foo() {
                mkdir -p ${TMP}sjdsdasjdha
                ./configure
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            python do_bar() {
                import os
                print("fooooooo!!!!")
            }
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)