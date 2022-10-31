import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsLicenseFilePrefix(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.licfileprefix'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'LIC_FILES_CHKSUM = "file://${S}/LICENSE;md5=a4a2bbea1db029f21b3a328c7a059172"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.licfileprefix'])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'LIC_FILES_CHKSUM = "file://${S}/LICENSE;md5=a4a2bbea1db029f21b3a328c7a059172"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'LIC_FILES_CHKSUM = "file://${S}LICENSE;md5=a4a2bbea1db029f21b3a328c7a059172"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     LIC_FILES_CHKSUM = "\\
                                         file://${S}/LICENSE;md5=a4a2bbea1db029f21b3a328c7a059172 \\
                                         file://${S}/COPYING;md5=a4a2bbea1db029f21b3a328c7a059172 \\
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_fix(self, input_, id_):
        self.fix_and_check(self._create_args_fix(input_), id_)

    @pytest.mark.parametrize('id_', ['oelint.vars.licfileprefix'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'LIC_FILES_CHKSUM = "file://LICENSE;md5=a4a2bbea1db029f21b3a328c7a059172"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'LIC_FILES_CHKSUM = "file://${WORKDIR}/LICENSE;md5=a4a2bbea1db029f21b3a328c7a059172"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
