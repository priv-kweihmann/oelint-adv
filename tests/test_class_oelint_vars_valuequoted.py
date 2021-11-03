import pytest
from base import TestBaseClass


class TestClassOelintVarsValueQuoted(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.valuequoted'])
    @pytest.mark.parametrize('occurrence', [2])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "a
            D = a"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.valuequoted'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "a"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A += "b"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            PACKAGECONFIG[foo] = "-DFOO=ON,-DFOO=OFF,"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            EXTRA_OECMAKE += "\\
                -DBUILD_TESTS=OFF \\
            "
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            DEPENDS += "\\
            a \\
            b \\    
            c \\
            "
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
