import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintTaskNoMkdir(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.task.nomkdir'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_install() {
                mkdir -p ${TMP}sjdsdasjdha
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                mkdir -p ${TMP}sjdsdasjdha
            }
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.nomkdir'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_install() {
                install -d ${TMP}sjdsdasjdha
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_compile() {
                mkdir -p ${TMP}sjdsdasjdha
            }
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)