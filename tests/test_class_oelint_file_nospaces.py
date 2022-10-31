import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintFileNoSpaces(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.file.nospaces'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
