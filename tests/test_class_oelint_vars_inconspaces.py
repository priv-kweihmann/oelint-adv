import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsInconSpaces(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.inconspaces'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            VAR += " ffjjj"
            '''
            },
                        {
            'oelint_adv_test.bb':
            '''
            VAR_append = "fhhh"
            '''
            },
                        {
            'oelint_adv_test.bb':
            '''
            RDEPENDS:${PN}-ptest:append:libc-glibc = "\\
            locale-base-en-us.iso-8859-1 \\
            "
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.inconspaces'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            VAR += "ffjjj"
            '''
            },
                        {
            'oelint_adv_test.bb':
            '''
            VAR_append = " fhhh"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILESEXTRAPATHS_append := "foo:"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            RDEPENDS:${PN}-ptest:append:libc-glibc = "\\
                locale-base-en-us.iso-8859-1 \\
            "
            '''
            },
                        {
            'oelint_adv_test.bb':
            '''
            A += "\\
                foo \\
            "
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
