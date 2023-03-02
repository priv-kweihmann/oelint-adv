import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsSRCURIReqOpt(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "git://foo.org/gaz.git;name=foo;branch=master"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "gitsm://foo.org/gaz.git;name=foo;branch=master"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "git://foo.org/gaz.git;name=foo;protocol=ssh"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "gitsm://foo.org/gaz.git;name=foo;protocol=ssh"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [2])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "git://foo.org/gaz.git;name=foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "gitsm://foo.org/gaz.git;name=foo"',
                                 },
                             ],
                             )
    def test_really_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "git://foo.org/gaz.git;name=foo;protocol=ssh;branch=main"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "gitsm://foo.org/gaz.git;name=foo;protocol=ssh;branch=main"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "git://foo.org/gaz.git;name=foo;protocol=ssh;nobranch=1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "gitsm://foo.org/gaz.git;name=foo;protocol=ssh;nobranch=1"',
                                 },
                                 {
                                     'oelint-adv_test.bb':
                                     '''
                                     SRC_REPO ?= "bitbucket.org/foo/bar.git"
                                     GIT_PROTO ?= "user=git;protocol=ssh"
                                     GIT_SUBPATH ?= "subpath=tools/${PACKAGE_NAME}"
                                     SRC_URI = "git://${SRC_REPO};nobranch=1;${GIT_PROTO};${GIT_SUBPATH}"
                                     SRCREV ?= "master"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
