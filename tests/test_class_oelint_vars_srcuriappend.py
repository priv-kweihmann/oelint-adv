import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsSRCURIappend(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.srcuriappend'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "file://abc"
                                     inherit abc
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI  += "file://abc"
                                     inherit abc
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcuriappend'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "file://abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI  += "file://abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI_append = " file://abc"
                                     inherit abc
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI_remove = "file://abc"
                                     inherit abc
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI:append = " file://abc"
                                     inherit abc
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI:remove = "file://abc"
                                     inherit abc
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI_prepend = "file://abc "
                                     inherit abc
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit abc
                                     SRC_URI[md5sum] = "1234"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit abc
                                     SRC_URI[sha256sum] = "1234"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
