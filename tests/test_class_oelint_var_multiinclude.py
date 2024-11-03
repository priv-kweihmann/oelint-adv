import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarMultiInclude(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.var.multiinclude'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     include abc.inc
                                     B = "2"
                                     include abc.inc
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     require abc.inc
                                     B = "2"
                                     include abc.inc
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     require abc.inc
                                     B = "2"
                                     include abc.inc
                                     ''',
                                     'abc.inc':
                                     '''
                                     A = "1"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.multiinclude'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     include abc.inc
                                     B = "2"
                                     include abc2.inc
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     include abc.inc
                                     ''',
                                     'abc.inc':
                                     '''
                                     A = "1"
                                     ''',
                                     'dynamic-layers/test/oelint_adv_test.bb':
                                     '''
                                     include abc.inc
                                     ''',
                                     'dynamic-layers/test/abc.inc':
                                     '''
                                     A = "1"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
