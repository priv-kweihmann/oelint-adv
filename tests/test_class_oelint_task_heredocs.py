import pytest
from .base import TestBaseClass


class TestClassOelintTaskHeredocs(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.task.heredocs'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_foo() {
                cat    >  ${T}/some.files <<   abchhehdhhe
                kfkdfkd
                abchhehdhhe
            }
            '''
            },
                        {
            'oelint_adv_test.bb':
            '''
            do_install_append() {
                cat    <<   EOF    >${T}/some.files
                abc
                EOF
            }
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.task.heredocs'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            do_install() {
                abc
            }
            '''
            }
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
