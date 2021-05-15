import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsMispell(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.mispell'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            DPENDS += "foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILS = "foo"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.mispell'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            RDEPENDS_${PN} = "foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            PACKAGECONFIG[foo] = "a"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            GOPATH = "abc"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            PACKAGECONFIG_A = "a"
            PACKAGECONFIG_B = "c"

            do_configure() {
                ./configure ${PACKAGECONFIG_A}
            }

            python do_foo() {
                d.getVar("PACKAGECONFIG_B")
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            PACKAGES += "${PN}-foo"
            INITSCRIPT_PARAMS_${PN}-foo = "bar"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)