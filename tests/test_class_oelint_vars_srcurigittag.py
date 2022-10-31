import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsSRCURIGitTag(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurigittag'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "git://foo.org/gaz.git;tag=${PV};name=foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "git://foo.org/gaz.git;tag=${PV}"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurigittag'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "git://abc.group.com/a.git"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "ftp://abc.group.com/some.patch"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "${@["", "file://init.cfg"][(d.getVar(\'VIRTUAL-RUNTIME_init_manager\') == \'busybox\')]}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "svn://foo.org/gaz.git;tag=${PV};name=foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "git://foo.org/gaz.git;name=foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI[md5sum] = "file://abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI[sha256sum] = "file://abc"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
