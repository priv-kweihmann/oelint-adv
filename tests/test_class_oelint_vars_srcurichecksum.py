import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsSRCURICHECKSUM(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurichecksum'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "ftp://foo;name=f3"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "ftp://foo;name=f3"
                                     SRC_URI += "ftp://foo;name=f2"
                                     SRC_URI[f3.sha256sum] = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "ftp://foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "ftp://foo"
                                     SRC_URI[sha256sum] = "a"
                                     SRC_URI[md5sum] = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "ftp://foo;name=f3"
                                     SRC_URI[f3.sha256sum] = "a"
                                     SRC_URI[f3.md5sum] = "a"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurichecksum'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "file://foo"
                                     SRC_URI += "bzr://foo"
                                     SRC_URI += "crcc://foo"
                                     SRC_URI += "cvs://foo"
                                     SRC_URI += "ftp://foo;name=f3"
                                     SRC_URI += "git://foo;name"
                                     SRC_URI += "gitsm://foo"
                                     SRC_URI += "gitannex://foo"
                                     SRC_URI += "hg://foo"
                                     SRC_URI += "http://foo;name=f1"
                                     SRC_URI += "https://foo;name=f2"
                                     SRC_URI += "osc://foo"
                                     SRC_URI += "p4://foo"
                                     SRC_URI += "repo://foo"
                                     SRC_URI += "ssh://foo"
                                     SRC_URI += "s3://foo;name=f5"
                                     SRC_URI += "sftp://foo;name=f4"
                                     SRC_URI += "npm://foo"
                                     SRC_URI += "svn://foo"
                                     SRC_URI += "az://foo;name=f6"
                                     SRC_URI[f1.sha256sum] = "a"
                                     SRC_URI[f2.sha256sum] = "a"
                                     SRC_URI[f3.sha256sum] = "a"
                                     SRC_URI[f4.sha256sum] = "a"
                                     SRC_URI[f5.sha256sum] = "a"
                                     SRC_URI[f6.sha256sum] = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "file://foo"
                                     SRC_URI += "bzr://foo"
                                     SRC_URI += "crcc://foo"
                                     SRC_URI += "cvs://foo"
                                     SRC_URI += "ftp://foo;sha256sum=a"
                                     SRC_URI += "git://foo;name"
                                     SRC_URI += "gitsm://foo"
                                     SRC_URI += "gitannex://foo"
                                     SRC_URI += "hg://foo"
                                     SRC_URI += "http://foo;sha256sum=a"
                                     SRC_URI += "https://foo;sha256sum=a"
                                     SRC_URI += "osc://foo"
                                     SRC_URI += "p4://foo"
                                     SRC_URI += "repo://foo"
                                     SRC_URI += "ssh://foo"
                                     SRC_URI += "s3://foo;sha256sum=a"
                                     SRC_URI += "sftp://foo;sha256sum=a"
                                     SRC_URI += "npm://foo"
                                     SRC_URI += "svn://foo"
                                     SRC_URI += "az://foo;sha256sum=a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "ftp://foo \\
                                                 ftp://foo;name=f1"
                                     SRC_URI[sha256sum] = "a"
                                     SRC_URI[f1.sha256sum] = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "${@["", "file://init.cfg"][(d.getVar(\'VIRTUAL-RUNTIME_init_manager\') == \'busybox\')]}"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "http://foo;name=f1"
                                     SRC_URI[f1.sha256sum] = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "ftp://foo"
                                     SRC_URI[sha256sum] = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "https://foo;name=f2"
                                     SRC_URI[f2.sha256sum] = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "ftp://foo"
                                     SRC_URI[sha256sum] = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     CUSTOM_VAR[md5sum] = "a"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
