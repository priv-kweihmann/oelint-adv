import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsSRCURIfile(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurifile'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "file://abc"
                                     SRC_URI += "git://foo.org/gaz.git"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "file://abc"
                                     SRC_URI += "http://foo.org/abc.tar.gz"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "file://abc"
                                     inherit foo
                                     SRC_URI += "http://foo.org/abc.tar.gz"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "http://def.com/bar.zip"
                                     SRC_URI:prepend = "file://abc"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI:append = "file://abc"
                                     SRC_URI:append = "http://def.com/bar.zip"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurifile'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "${@do_magic_function(d)} file://abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "file://abc"
                                     SRC_URI += "file://def"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "file://abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "file://abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "file://foo ${@bb.utils.contains(\'FOO\', \'bar\', \'file://bar\', \'\', d)}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI[sha256sum] = "file://abc"',
                                 },
                                 {
                                     'recipes/oelint_adv_test.bb':
                                     '''
                                     A = "1"
                                     inherit foo
                                     ''',
                                     'conf/layer.conf':
                                     ' ',
                                     'classes/foo.bbclass':
                                     'SRC_URI ?= "https://some.corp.org/${PN}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI:append = "file://abc"
                                     SRC_URI += "http://def.com/bar.zip"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
