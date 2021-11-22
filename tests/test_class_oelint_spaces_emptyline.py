import pytest

from .base import TestBaseClass


class TestClassOelintSpacesEmptyLine(TestBaseClass):
    @pytest.mark.parametrize('id', ['oelint.spaces.emptyline'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                      
                                     B = "1"
                                     ''',  # noqa: W293 - this is exactly what we want to test
                                 },
                             ],
                             )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
