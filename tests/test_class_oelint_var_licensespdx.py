import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarLicenseSPDX(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.licensesdpx'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     LICENSE:a = "ISC &MIT"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     LICENSE:e = "(ISC|MIT) & Apache-2.0 & BSD-3-Clause"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.licensesdpx'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     LICENSE:${PN} = "BSD-2-Clause"
                                     LICENSE:b = "(ISC | MIT)"
                                     LICENSE:c = "(BSD-2-Clause | MIT)"
                                     LICENSE:d = "(BSD-2-Clause | MIT) & MIT"
                                     LICENSE:f = "BSD-3-Clause"
                                     LICENSE = "Unknown"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
