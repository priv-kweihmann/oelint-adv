import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintSpacesEmptyLine(TestBaseClass):
    @pytest.mark.parametrize('id_', ['oelint.spaces.emptyline'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
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
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
