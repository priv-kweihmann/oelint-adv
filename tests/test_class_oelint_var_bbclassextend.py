import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarBBClassExtend(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.var.bbclassextend'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'A = "1"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.bbclassextend'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'BBCLASSEXTEND = "native"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'BBCLASSEXTEND = "native nativesdk"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     '',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit native',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit cross',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit nativesdk',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit core-image',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit packagegroup',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
