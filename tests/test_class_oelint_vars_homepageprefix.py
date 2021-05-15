import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsHomepagePrefix(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.homepageprefix'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            HOMEPAGE = "ftp://isnt/21stcentury/tech"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            HOMEPAGE = "abc"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            HOMEPAGE = "ssh://wont/get/u/anywhere"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.homepageprefix'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bbappend':
            '''
            HOMEPAGE = "http://fancy.org"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            HOMEPAGE = "https://fancy.org"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            HOMEPAGE = " https://evenmore.fancy.org"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)