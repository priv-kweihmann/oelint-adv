import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintTaskMultiAppends(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.task.multifragments'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                a
            }
            do_install_append() {
                b
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_configure_append() {
                a
            }
            do_configure_append() {
                b
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_custom_append() {
                a
            }
            do_custom_append() {
                b
            }
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.multifragments'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                a
            }
            do_install_append_class-native() {
                a
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                a
            }
            do_install_append_class-nativesdk() {
                a
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                a
            }
            do_install_append_class-cross() {
                a
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                a
            }
            do_install_append_class-target() {
                a
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                a
            }
            do_install_prepend() {
                a
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                a
            }
            do_somethingelse_append() {
                a
            }
            '''
            }
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)