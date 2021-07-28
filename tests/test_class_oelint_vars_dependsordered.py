import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsDependsOrdered(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.dependsordered'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS += "zzz \\
            xyz"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS += "foo"
            DEPENDS += "bar"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            RDEPENDS_${PN} += "zzz \\
                        xyz"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            RDEPENDS_${PN} += "foo"
            RDEPENDS_${PN} += "bar"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.dependsordered'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS += "bar"
            DEPENDS += "foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS += "xyz \\
                        zzz"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            RDEPENDS_${PN} += "bar"
            RDEPENDS_${PN} += "foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            RDEPENDS_${PN} += "xyz \\
                        zzz"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS_class-native += "\\
                rubygems-mini-portile2-native \\
                rubygems-racc-native \\
            "
            DEPENDS_class-target += "\\
                rubygems-mini-portile2 \\
            "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS += "a (>= 1.2.3) \\
                        b (>= 4.5.6)"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)