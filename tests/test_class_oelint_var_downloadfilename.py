import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarDownloadfilename(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.downloadfilename'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "http://foo.bar/baz.jpg"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "https://foo.bar/baz.jpg"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "ftp://foo.bar/baz.jpg"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "http://foo.bar/baz.jpg;downloadfilename=something.dat"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.downloadfilename'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "http://foo.bar/baz.jpg;downloadfilename=something.dat.${PV}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "http://foo.bar/baz1.0.jpg"',
                                 },
                                 {
                                     'oelint_adv_test_1.2.3.bb':
                                     'SRC_URI += "http://foo.bar/baz1.2.3.jpg"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "git://foo.bar/baz.git"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "http://foo.bar/baz.jpg;downloadfilename=something.${PV}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     PV = "1.2.3"
                                     SRC_URI += "http://foo.bar/baz.jpg;downloadfilename=something.1.2.3"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
