import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsFileSettingsDouble(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.filessetting.double'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILES:${PN} += "${bindir}"
                                     FILES:${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     '''
                                     FILES:${PN} += "${bindir}"
                                     FILES:${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILES:${PN} += "${bindir}"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILES:${PN}-doc += "${docdir}"
                                     ''',
                                 },

                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.filessetting.double'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILES_${PN} += "${bindir}"
                                     FILES_${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     '''
                                     FILES_${PN} += "${bindir}"
                                     FILES_${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILES_${PN} += "${bindir}"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILES_${PN}-doc += "${docdir}"
                                     ''',
                                 },
                             ],
                             )
    def test_bad_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.filessetting.double'])
    @pytest.mark.parametrize('occurrence', [2])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILES:${PN} += "/opt/other/path"
                                     FILES:${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     FILES:${PN} += "/opt/other/path"
                                     ''',
                                 },
                             ],
                             )
    def test_bad_non_default(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.filessetting.double'])
    @pytest.mark.parametrize('occurrence', [2])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILES_${PN} += "/opt/other/path"
                                     FILES_${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     FILES_${PN} += "/opt/other/path"
                                     ''',
                                 },
                             ],
                             )
    def test_bad_non_default_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.filessetting.double'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILES:${PN} += "/opt/other/path"
                                     FILES:${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.filessetting.double'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILES_${PN} += "/opt/other/path"
                                     FILES_${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     ''',
                                 },
                             ],
                             )
    def test_good_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)
