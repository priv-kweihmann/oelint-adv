import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsInconSpaces(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.inconspaces'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'VAR += " ffjjj"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'VAR:append = "fhhh"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN}-ptest:append:libc-glibc = "\\
                                     locale-base-en-us.iso-8859-1 \\
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.inconspaces'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'VAR_append = "fhhh"',
                                 },
                             ],
                             )
    def test_bad_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.inconspaces'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'VAR += "ffjjj"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILESEXTRAPATHS_append := "foo:"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'VAR:append = " fhhh"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILESEXTRAPATHS:append := "foo:"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN}-ptest:append:libc-glibc = "\\
                                         locale-base-en-us.iso-8859-1 \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A += "\\
                                         foo \\
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.inconspaces'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'VAR_append = " fhhh"',
                                 },
                             ],
                             )
    def test_good_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)
