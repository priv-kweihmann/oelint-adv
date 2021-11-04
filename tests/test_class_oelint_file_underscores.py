import pytest
from .base import TestBaseClass


class TestClassOelintFileUnderscores(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.file.underscores'])
    @pytest.mark.parametrize('occurrence', [1])
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
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.file.underscores'])
    @pytest.mark.parametrize('occurrence', [0])
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
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

