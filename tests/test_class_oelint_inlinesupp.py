import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintNAInlineSuppression(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.file.inlinesuppress_na'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     # nooelint: oelint.var.badimagefeature
                                     A = "2"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     # nooelint: oelint.vars.mispell, oelint.var.badimagefeature
                                     SRR_URI = "2"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.inlinesuppress_na'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo() {
                                         :
                                     }
                                     addtask do_foo
                                     do_foo[doc] = "Fooo!!!!"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     # nooelint: oelint.vars.mispell
                                     SRR_URI = "2"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
