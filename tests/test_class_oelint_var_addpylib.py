import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarAddpylib(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.var.addpylib'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'addpylib ${LAYERDIR}/foo a',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'addpylib ${LAYERDIR}/foo a',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.addpylib'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.conf':
                                     'addpylib ${LAYERDIR}/foo a',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
