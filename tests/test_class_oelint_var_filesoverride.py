import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarFilesOverride(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.var.filesoverride'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            FILES_${PN} = " foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILES_${PN} := "foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILES_${PN}-dev = "foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILES_${PN}-dev := "foo"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.var.filesoverride'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bbappend':
            '''
            FILES_SOLIBSDEV = "abc"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILES_${PN}_append = " foo"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILES_${PN}_prepend = "foo "
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILES_${PN} += "foo"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILES_${PN} =+ "foo"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILES_${PN} .= " foo"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILES_${PN} =. "foo "
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILES_${PN}-dev += "foo"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILES_${PN}-dev =+ "foo"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILES_${PN}-dev .= " foo"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILES_${PN}-dev =. "foo "
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)