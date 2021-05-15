import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintFileUpstreamStatus(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.file.upstreamstatus'])
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
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Acceppted
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Submit
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [me don't care]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate
            ''',
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)


    @pytest.mark.parametrize('id', ['oelint.file.upstreamstatus'])
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
            Upstream-Status: Accepted
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Backport
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Denied
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [bugfix this is a bugfix]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [configuration]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [disable feature]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [embedded specific]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [enable feature]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [licensing]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [native]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [no upstream]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [other]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Pending
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Submitted [http://some.where]
            ''',
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

