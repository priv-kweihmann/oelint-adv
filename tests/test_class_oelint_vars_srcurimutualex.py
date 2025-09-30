import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarSRCURIMutualExItems(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurimutualex'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "gitsm://github.com/CLIUtils/CLI11;branch=main;protocol=https"
                                     SRCREV = "1233454566789"
                                     SRC_URI[sha256sum] = "1233454566789"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "gitsm://github.com/CLIUtils/CLI11;branch=main;protocol=https;name=foo"
                                     SRCREV_foo = "1233454566789"
                                     SRC_URI[foo.sha256sum] = "1233454566789"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "gitsm://github.com/CLIUtils/CLI11;branch=main;protocol=https;name=foo"
                                     SRCREV_foo = "1233454566789"
                                     SRCREV = "21233454566789"
                                     SRC_URI[foo.sha256sum] = "1233454566789"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurimutualex'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "gitsm://github.com/CLIUtils/CLI11;branch=main;protocol=https"
                                     SRCREV = "21233454566789"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "gitsm://github.com/CLIUtils/CLI11;branch=main;protocol=https"
                                     SRC_URI[sha256sum] = "21233454566789"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "gitsm://github.com/CLIUtils/CLI11;branch=main;protocol=https"
                                     SRC_URI[md5sum] = "21233454566789"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "gitsm://github.com/CLIUtils/CLI11;branch=main;protocol=https"
                                     SRC_URI[magicalsum] = "21233454566789"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "gitsm://github.com/CLIUtils/CLI11;branch=main;protocol=https"
                                     SRC_URI[otherflag] = "21233454566789"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
