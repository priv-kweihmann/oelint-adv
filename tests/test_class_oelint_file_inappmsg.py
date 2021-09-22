import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintFileUpstreamStatusInAppMsg(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.file.inappropriatemsg'])
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
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate (configuration)
            ''',
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.file.inappropriatemsg'])
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
            Upstream-Status: Inappropriate [oe-specific]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [OE specific]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [oe-core specific]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [not author]
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
            Upstream-Status: Inappropriate [bugfix this and that]
            ''',
            },
            {
            'oelint_adv-test.bb':
            '''
            SRC_URI = "file://test.patch"
            ''',
            'files/test.patch':
            '''
            Upstream-Status: Inappropriate [bugfix #12345]
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
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

