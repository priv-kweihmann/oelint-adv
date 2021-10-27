import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarRootFSCmd(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.var.rootfspostcmd'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            ROOTFS_POSTPROCESS_COMMAND += "abc; adef ;;"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.var.rootfspostcmd'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            ROOTFS_POSTPROCESS_COMMAND += "abc; adef;;"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
