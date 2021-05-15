import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsPBPUsage(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.pbpusage'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "file://${P}.patch"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "git://${P}.com/${P}.git"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "https://foo.org/${P}"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            S = "${WORDKIR}/${P}"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.pbpusage'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "file://${BP}.patch"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "git://${BP}.com/${BP}.git"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "https://foo.org/${BP}"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            S = "${WORDKIR}/${BP}"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRCREV_${P} = "01234567890abcdef"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)