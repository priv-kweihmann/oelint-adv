import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsSRCURIdomains(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.srcuridomains'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "git://abc.group.com/a.git"
                                     SRC_URI += "git://def.group.com/b.git"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI:class-devupstream = "git://foo.bar;branch=master;protocol=https"
                                     SRC_URI:append:class-devupstream = " git://foo.baz;branch=master;protocol=https"
                                     SRC_URI:remove:class-devupstream:qemuall = "git://foo.baz;branch=master;protocol=https"
                                     SRC_URI = "git://foo.baz;branch=master;protocol=https"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI:class-devupstream = "git://foo.bar;branch=master;protocol=https"
                                     SRC_URI:append:class-devupstream = " git://foo.baz;branch=master;protocol=https"
                                     SRC_URI = "git://foo.baz;branch=master;protocol=https"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcuridomains'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "git://abc.group.com/a.git"
                                     SRC_URI += "ftp://abc.group.com/some.patch"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "git://abc.group.com/a.git"
                                     SRC_URI += "file://some.patch"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "ftp://abc.group.com/some.patch"
                                     SRC_URI += "${@["", "file://init.cfg"][(d.getVar('VIRTUAL-RUNTIME_init_manager') == 'busybox')]}"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI:class-devupstream = "git://foo.bar;branch=master;protocol=https"
                                     SRC_URI:remove:class-devupstream = "git://foo.baz;branch=master;protocol=https"
                                     SRC_URI = "git://foo.baz;branch=master;protocol=https"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI:class-devupstream = "git://foo.bar;branch=master;protocol=https"
                                     SRC_URI:remove:class-devupstream = "git://foo.bar;branch=master;protocol=https"
                                     SRC_URI = "git://foo.baz;branch=master;protocol=https"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI:class-devupstream = "git://foo.bar;branch=master;protocol=https"
                                     SRC_URI = "git://foo.baz;branch=master;protocol=https"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI:class-devupstream = "git://foo.baz;branch=master;protocol=https"
                                     SRC_URI = "git://foo.baz;branch=master;protocol=https"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI:append:class-devupstream = " git://foo.baz;branch=master;protocol=https"
                                     SRC_URI = "git://foo.baz;branch=master;protocol=https"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
