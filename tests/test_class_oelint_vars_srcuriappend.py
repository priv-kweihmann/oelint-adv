import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsSRCURIappend(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.srcuriappend'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "file://abc"
            inherit abc
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.srcuriappend'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "file://abc"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI_append = " file://abc"
            inherit abc
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI_remove = "file://abc"
            inherit abc
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI_prepend = "file://abc "
            inherit abc
            "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit abc
            SRC_URI[md5sum] = "1234"
            "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit abc
            SRC_URI[sha256sum] = "1234"
            "
            '''
            }
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)