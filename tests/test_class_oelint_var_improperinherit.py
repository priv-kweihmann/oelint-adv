import pytest
from .base import TestBaseClass


class TestClassOelintVarImproperInherit(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.var.improperinherit'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            inherit abc/abc abc
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit def~AAAA
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit ghi>bbclass
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.var.improperinherit'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            inherit abc def
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit A0_a
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit update-rc.d
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit ${@magic_call(d)}
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            XORGBUILDCLASS ??= "autotools"
            inherit ${XORGBUILDCLASS} pkgconfig features_check
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
