import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintTaskHeredocs(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.task.heredocs'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_foo() {
                cat    >  ${T}/some.files <<   abchhehdhhe
                kfkdfkd
                abchhehdhhe
            }
            '''
            },
                        {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                cat    <<   EOF    >${T}/some.files
                abc
                EOF
            }
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.heredocs'])
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
            }
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)