import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsSRCURIRevTag(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurisrcrevtag'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "git://foo.org/gaz.git;tag=${PV};name=foo"
                                     SRCREV_foo = "1234"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "git://foo.org/gaz.git;tag=${PV}"
                                     SRCREV = "1234"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurisrcrevtag'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "git://foo.org/gaz.git;name=bar"
                                     SRCREV_bar = "1234"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "git://foo.org/gaz.git"
                                     SRCREV = "1234"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "git://foo.org/gaz.git;tag=${PV};name=foo"
                                     SRCREV_bar = "1234"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI[md5sum] = "file://abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI[sha256sum] = "file://abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "${@magic.foo.operation}"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
