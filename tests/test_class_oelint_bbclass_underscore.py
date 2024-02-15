import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintBBClassUnderscore(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.bbclass.underscores'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'classes/oelint-test.bbclass':
                                     'VAR = "1"',
                                     'conf/layer.conf':
                                     '',
                                     'oelint_test.bb':
                                     'inherit oelint-test',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.bbclass.underscores'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'classes/oelint_test.bbclass':
                                     'VAR = "1"',
                                     'conf/layer.conf':
                                     '',
                                     'oelinttest.bb':
                                     'inherit oelint_test',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
