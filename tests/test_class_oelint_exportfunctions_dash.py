import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassExportFunctionsBash(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.exportfunction.dash'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bbclass':
                                     '''
                                     EXPORT_FUNCTIONS do-install
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bbclass':
                                     '''
                                     EXPORT_FUNCTIONS do-install do_something
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bbclass':
                                     '''
                                     EXPORT_FUNCTIONS do_something do-install
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.exportfunction.dash'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bbclass':
                                     '''
                                     EXPORT_FUNCTIONS do_something do_install
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bbclass':
                                     '''
                                     EXPORT_FUNCTIONS do_something
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
