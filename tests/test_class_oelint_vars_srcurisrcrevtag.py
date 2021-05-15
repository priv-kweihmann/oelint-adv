import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsSRCURIRevTag(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.srcurisrcrevtag'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://foo.org/gaz.git;tag=${PV};name=foo"
            SRCREV_foo = "1234"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://foo.org/gaz.git;tag=${PV}"
            SRCREV = "1234"
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.srcurisrcrevtag'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://foo.org/gaz.git;name=bar"
            SRCREV_bar = "1234"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://foo.org/gaz.git"
            SRCREV = "1234"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://foo.org/gaz.git;tag=${PV};name=foo"
            SRCREV_bar = "1234"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI[md5sum] = "file://abc"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI[sha256sum] = "file://abc"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "${@magic.foo.operation}"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)