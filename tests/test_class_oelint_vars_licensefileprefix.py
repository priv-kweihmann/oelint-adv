import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsLicenseFilePrefix(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.licfileprefix'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            LIC_FILES_CHKSUM = "file://${S}/LICENSE;md5=a4a2bbea1db029f21b3a328c7a059172"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.licfileprefix'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            LIC_FILES_CHKSUM = "file://LICENSE;md5=a4a2bbea1db029f21b3a328c7a059172"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            LIC_FILES_CHKSUM = "file://${WORKDIR}/LICENSE;md5=a4a2bbea1db029f21b3a328c7a059172"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)