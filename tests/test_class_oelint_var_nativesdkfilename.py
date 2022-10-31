import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarNativeSDKFilename(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.var.nativesdkfilename'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit nativesdk',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.nativesdkfilename'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'nativesdk-oelint-adv-test.bb':
                                     'inherit nativesdk',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
