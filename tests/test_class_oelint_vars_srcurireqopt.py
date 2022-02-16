import pytest

from .base import TestBaseClass


class TestClassOelintVarsSRCURIReqOpt(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input',
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
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [2])
    @pytest.mark.parametrize('input',
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
    def test_really_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input',
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
                             ],
                             )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
