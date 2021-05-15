import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsSRCURIdomains(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.srcuridomains'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://abc.group.com/a.git"
            SRC_URI += "git://def.group.com/b.git"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.srcuridomains'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://abc.group.com/a.git"
            SRC_URI += "ftp://abc.group.com/some.patch"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "ftp://abc.group.com/some.patch"
            SRC_URI += "${@["", "file://init.cfg"][(d.getVar('VIRTUAL-RUNTIME_init_manager') == 'busybox')]}"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)