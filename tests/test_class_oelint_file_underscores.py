import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintFileUnderscores(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.file.underscores'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv-test.bb':
            '''
            VAR = "1"
            '''
            },
            {
            'oelintadvtest.bb':
            '''
            VAR = "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            VAR = "1"
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.file.underscores'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            inherit core-image
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit image
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            IMAGE_INSTALL += "foo"
            '''
            },
            {
            'oelint-adv_1.2.3.bb':
            '''
            VAR = "a"
            '''
            },
            {
            'oelint-adv_git.bb':
            '''
            VAR = "a"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

