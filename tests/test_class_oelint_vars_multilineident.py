import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsMultilineIdent(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.multilineident'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "\\
                                         a \\
                                     b \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     D = "a \\
                                     e \\
                                         "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     D = "    a \\
                                          e \\
                                         "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "a \\
                                       b \\
                                          c \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "\\
                                         b \\
                                          c \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:append = "a \\
                                              b \\
                                                 c \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A += "a \\
                                        b \\
                                           c \\
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.multilineident'])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     D = "a \\
                                      e \\
                                         "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     D = "    a \\
                                         e \\
                                         "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "a \\
                                       b \\
                                          c \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:append = "a \\
                                              b \\
                                                 c \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A += "a \\
                                        b \\
                                           c \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:append = " \\
                                        b \\
                                           c \\
                                          "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:append = " \\
                                        b \\
                                           c \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "d \\
                                        b \\
                                           c \\
                                       "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "d \\
                                        b \\
                                           c"
                                     ''',
                                 },
                             ],
                             )
    def test_fix(self, input_, id_):
        self.fix_and_check(self._create_args_fix(input_), id_)

    @pytest.mark.parametrize('id_', ['oelint.vars.multilineident'])
    @pytest.mark.parametrize('occurrence', [2])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "a \\
                                     b \\
                                     c \\
                                         "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     D = "a \\
                                     e \\
                                     f \\
                                         "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "\\
                                     a \\
                                     b \\
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_bad_two(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.multilineident'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "\\
                                         a \\
                                         b \\
                                         e \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "a \\
                                          b \\
                                          c \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:append = "a \\
                                                 b \\
                                                 c \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A += "a \\
                                           b \\
                                           c \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "\\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "\\
                                         some \\"quoted\\" value \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "a \\
                                          some \\"quoted\\" value \\
                                         "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "a \\
                                          b"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "a \\
                                          b"
                                     B = "a \\
                                          b"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "
                                         a \\
                                         b
                                     "
                                     B = "
                                         a \\
                                         b"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     # nooelint: oelint.vars.multilineident
                                     A = "d \\
                                        b \\
                                           c"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
