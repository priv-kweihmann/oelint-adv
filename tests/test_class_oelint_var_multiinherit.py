import pytest
from base import TestBaseClass


class TestClassOelintVarMultiInherit(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.var.multiinherit'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            inherit abc abc
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit def
            inherit ghi def
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.var.multiinherit'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            inherit abc def
            inherit autotools \\
                    gobject-introspection \\
                    pkgconfig
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
