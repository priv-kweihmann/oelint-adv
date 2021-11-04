import pytest
from .base import TestBaseClass


class TestClassOelintVarsHomepagePrefix(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.homepageprefix'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            HOMEPAGE = "ftp://isn't/21stcentury/tech"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            HOMEPAGE = "abc"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            HOMEPAGE = "ssh://won't/get/u/anywhere"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.homepageprefix'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bbappend':
            '''
            HOMEPAGE = "http://fancy.org"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            HOMEPAGE = "https://fancy.org"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            HOMEPAGE = " https://evenmore.fancy.org"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
