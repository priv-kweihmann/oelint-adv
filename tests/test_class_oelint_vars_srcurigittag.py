import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsSRCURIGitTag(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.srcurigittag'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://foo.org/gaz.git;tag=${PV};name=foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://foo.org/gaz.git;tag=${PV}"
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.srcurigittag'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://abc.group.com/a.git"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "ftp://abc.group.com/some.patch"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "${@["", "file://init.cfg"][(d.getVar('VIRTUAL-RUNTIME_init_manager') == 'busybox')]}"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "svn://foo.org/gaz.git;tag=${PV};name=foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI += "git://foo.org/gaz.git;name=foo"
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
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)