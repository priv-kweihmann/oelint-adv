import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintFilePatchSignedOff(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.file.patchsignedoff'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            This is not a patch
            ''',
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.file.patchsignedoff'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Signed-off-by: some body <some@body.com>
            ''',
            }
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

