import pytest
from .base import TestBaseClass


class TestClassOelintVarsHomepagePing(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.homepageping'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            HOMEPAGE = "abc-def-ghi"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.homepageping'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bbappend':
            '''
            HOMEPAGE = "http://www.google.com"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
