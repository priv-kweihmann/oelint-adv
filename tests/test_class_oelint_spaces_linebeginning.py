import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintSpacesLineBeginning(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.spaces.linebeginning'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                      ABC = "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                         ABC = "1"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.spaces.linebeginning'])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                      ABC = "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                         ABC = "1"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def foo():
                                         return "abc"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo() {
                                         echo "abc"
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_fix(self, input_, id_):
        self.fix_and_check(self._create_args_fix(input_), id_)

    @pytest.mark.parametrize('id_', ['oelint.spaces.linebeginning'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'ABC = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def foo():
                                         return "abc"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo() {
                                         echo "abc"
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
