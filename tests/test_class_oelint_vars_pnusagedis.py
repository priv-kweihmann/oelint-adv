import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass


class TestClassOelintVarsPNUsageDiscouraged(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.pnusagediscouraged'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            HOMEPAGE = "http://${PN}.com"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            BUGTRACKER = "http://${PN}.com"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SUMMARY = "http://${PN}.com"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DESCRIPTION = "http://${PN}.com"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.pnusagediscouraged'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            HOMEPAGE = "http://some.org.com"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            BUGTRACKER = "http://${FOO}.com"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SUMMARY = "ssas"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DESCRIPTION = "1"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
