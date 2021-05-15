import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsListAppend(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.listappend'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            PACKAGES =. "foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILES_${PN}-tracepath_append = "${base_bindir}"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            RDEPENDS_${PN} .= "bar"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS_prepend = "xyz"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI .= "file://abc"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.listappend'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            PACKAGES =. "foo "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILES_${PN}-tracepath_append = " ${base_bindir}"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            RDEPENDS_${PN} .= " bar"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS_prepend = "xyz "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI .= " file://abc"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)