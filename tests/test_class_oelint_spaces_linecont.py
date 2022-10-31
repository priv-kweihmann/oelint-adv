import pytest  # noqa: I900

from .base import TestBaseClass

# flake8: noqa W291 - we want to explicitly test trailing whitespace here
class TestClassOelintSpacesLineCont(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.spaces.linecont'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     ABC = "1 \\ 
                                         "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "\\
                                        a \\
                                        b \\ 
                                        c \\
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.spaces.linecont'])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     ABC = "1 \\ 
                                         "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "\\
                                        a \\
                                        b \\ 
                                        c \\
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_fix(self, input_, id_):
        self.fix_and_check(self._create_args_fix(input_), id_)

    @pytest.mark.parametrize('id_', ['oelint.spaces.linecont'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "\\
                                        a \\
                                        b \\
                                        c \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     ABC = "1 \\
                                         "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     # this is just a comment \\ 
                                     # so don't mind that
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
