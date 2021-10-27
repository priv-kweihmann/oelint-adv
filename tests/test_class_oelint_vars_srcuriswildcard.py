import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarSRCURIWildcard(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.var.srcuriwildcard'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "file://*"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://foo.org;name=${PV} \\
                file://somedir/*"
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.var.srcuriwildcard'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "git://foo.org;name=${PV}"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "${@["", "file://init.cfg"][(d.getVar('VIRTUAL-RUNTIME_init_manager') == 'busybox')]}"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
