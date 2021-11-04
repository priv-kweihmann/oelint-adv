import pytest
from .base import TestBaseClass


class TestClassOelintSpacesLineBeginning(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.spaces.linebeginning'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
             ABC = "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
                ABC = "1"
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.spaces.linebeginning'])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
             ABC = "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            A = "1"
                ABC = "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            def foo():
                return "abc"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_foo() {
                echo "abc"
            }
            '''
            }
        ],
    )
    def test_fix(self, input, id):
        self.fix_and_check(self._create_args_fix(input), id)

    @pytest.mark.parametrize('id', ['oelint.spaces.linebeginning'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            ABC = "1"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            def foo():
                return "abc"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_foo() {
                echo "abc"
            }
            '''
            }
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
