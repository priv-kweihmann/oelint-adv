import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsFileSettingsHidden(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.filessetting.hidden'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SPLITPKGS = "${PN}-ping ${PN}-arping ${PN}-tracepath ${PN}-clockdiff \
                                                 ${PN}-tftpd ${PN}-rdisc \
                                                 ${@bb.utils.contains('PACKAGECONFIG', 'rarpd', '${PN}-rarpd', '', d)} \
                                                 ${@bb.utils.contains('DISTRO_FEATURES', 'ipv6', '${PN}-traceroute6 ${PN}-ninfod', '', d)}"
                                     PACKAGES += "${SPLITPKGS}"
                                     ALLOW_EMPTY:${PN} = "1"
                                     RDEPENDS_${PN} += "${SPLITPKGS}"
                                     FILES:${PN} += "${bindir}"
                                     FILES:${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     FILES:${PN}-arping = "${base_bindir}/arping"
                                     FILES:${PN}-tracepath = "${base_bindir}/tracepath"
                                     FILES:${PN}-traceroute6	= "${base_bindir}/traceroute6"
                                     FILES:${PN}-clockdiff = "${base_bindir}/clockdiff"
                                     FILES:${PN}-tftpd = "${bindir} ${base_bindir}/tftpd"
                                     FILES:${PN}-rarpd = "${base_sbindir}/rarpd  ${systemd_unitdir}/system/rarpd@.service"
                                     FILES:${PN}-rdisc = "${base_sbindir}/rdisc"
                                     FILES:${PN}-ninfod = "${base_sbindir}/ninfod ${sysconfdir}/init.d/ninfod.sh"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.filessetting.hidden'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SPLITPKGS = "${PN}-ping ${PN}-arping ${PN}-tracepath ${PN}-clockdiff \
                                      ${PN}-tftpd ${PN}-rdisc \
                                      ${@bb.utils.contains('PACKAGECONFIG', 'rarpd', '${PN}-rarpd', '', d)} \
                                      ${@bb.utils.contains('DISTRO_FEATURES', 'ipv6', '${PN}-traceroute6 ${PN}-ninfod', '', d)}"
                                     PACKAGES =+ "${SPLITPKGS}"

                                     ALLOW_EMPTY_${PN} = "1"
                                     RDEPENDS_${PN} += "${SPLITPKGS}"

                                     FILES_${PN} += "${bindir}"
                                     FILES_${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     FILES_${PN}-arping = "${base_bindir}/arping"
                                     FILES_${PN}-tracepath = "${base_bindir}/tracepath"
                                     FILES_${PN}-traceroute6	= "${base_bindir}/traceroute6"
                                     FILES_${PN}-clockdiff = "${base_bindir}/clockdiff"
                                     FILES_${PN}-tftpd = "${bindir} ${base_bindir}/tftpd"
                                     FILES_${PN}-rarpd = "${base_sbindir}/rarpd  ${systemd_unitdir}/system/rarpd@.service"
                                     FILES_${PN}-rdisc = "${base_sbindir}/rdisc"
                                     FILES_${PN}-ninfod = "${base_sbindir}/ninfod ${sysconfdir}/init.d/ninfod.sh"
                                     ''',
                                 },
                             ],
                             )
    def test_bad_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.filessetting.hidden'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SPLITPKGS = "${PN}-ping ${PN}-arping ${PN}-tracepath \
                                      ${PN}-clockdiff ${PN}-tftpd ${PN}-rdisc \
                                      ${@bb.utils.contains('PACKAGECONFIG', 'rarpd', '${PN}-rarpd', '', d)} \
                                      ${@bb.utils.contains('DISTRO_FEATURES', 'ipv6', '${PN}-traceroute6 ${PN}-ninfod', '', d)}"
                                     PACKAGES += "${SPLITPKGS}"
                                     ALLOW_EMPTY:${PN} = "1"
                                     RDEPENDS_${PN} += "${SPLITPKGS}"
                                     FILES:${PN} = ""
                                     FILES:${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     FILES:${PN}-arping = "${base_bindir}/arping"
                                     FILES:${PN}-tracepath = "${base_bindir}/tracepath"
                                     FILES:${PN}-traceroute6	= "${base_bindir}/traceroute6"
                                     FILES:${PN}-clockdiff = "${base_bindir}/clockdiff"
                                     FILES:${PN}-tftpd = "${bindir} ${base_bindir}/tftpd"
                                     FILES:${PN}-rarpd = "${base_sbindir}/rarpd  ${systemd_unitdir}/system/rarpd@.service"
                                     FILES:${PN}-rdisc = "${base_sbindir}/rdisc"
                                     FILES:${PN}-ninfod = "${base_sbindir}/ninfod ${sysconfdir}/init.d/ninfod.sh"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.filessetting.hidden'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SPLITPKGS = "${PN}-ping ${PN}-arping ${PN}-tracepath \
                                      ${PN}-clockdiff ${PN}-tftpd ${PN}-rdisc \
                                      ${@bb.utils.contains('PACKAGECONFIG', 'rarpd', '${PN}-rarpd', '', d)} \
                                      ${@bb.utils.contains('DISTRO_FEATURES', 'ipv6', '${PN}-traceroute6 ${PN}-ninfod', '', d)}"
                                     PACKAGES += "${SPLITPKGS}"
                                     ALLOW_EMPTY_${PN} = "1"
                                     RDEPENDS_${PN} += "${SPLITPKGS}"
                                     FILES_${PN} = ""
                                     FILES_${PN}-ping = "${base_bindir}/ping.${BPN}"
                                     FILES_${PN}-arping = "${base_bindir}/arping"
                                     FILES_${PN}-tracepath = "${base_bindir}/tracepath"
                                     FILES_${PN}-traceroute6	= "${base_bindir}/traceroute6"
                                     FILES_${PN}-clockdiff = "${base_bindir}/clockdiff"
                                     FILES_${PN}-tftpd = "${bindir} ${base_bindir}/tftpd"
                                     FILES_${PN}-rarpd = "${base_sbindir}/rarpd  ${systemd_unitdir}/system/rarpd@.service"
                                     FILES_${PN}-rdisc = "${base_sbindir}/rdisc"
                                     FILES_${PN}-ninfod = "${base_sbindir}/ninfod ${sysconfdir}/init.d/ninfod.sh"
                                     ''',
                                 },
                             ],
                             )
    def test_good_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)
