import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintTaskNoAnonPython(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.task.noanonpython'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            python __anonymous() {
                print("foo")
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            python () {
                print("bar")
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            python() {
                print("baz")
            }
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.noanonpython'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_install() {
                abc
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            python do_something_else() {
                :
            }
            addtask do_something_else
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)