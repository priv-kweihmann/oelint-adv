import pytest
from base import TestBaseClass


class TestClassOelintTaskNoCopy(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.task.nocopy'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                cp A B
            }
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                cp * B
            }
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.task.nocopy'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                install A B
            }
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
