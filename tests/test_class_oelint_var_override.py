import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarOverride(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.var.override'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                     A = "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                     B = "0"
                                     A = "1"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.override'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                     A += "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                     A =+ "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                     A .= "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                     A  += "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                     A =. "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                     A ?= "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                     A ??= "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A  = "1"
                                     A ??= "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILESEXTRAPATH_prepend := "a:"
                                     FILESEXTRAPATH_prepend := "b:"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILESEXTRAPATH_append := ":a"
                                     FILESEXTRAPATH_append := ":b"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     PACKAGECONFIG = "a b c"
                                     PACKAGECONFIG:remove = "a"
                                     PACKAGECONFIG:remove = "b"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
