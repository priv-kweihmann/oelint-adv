import pytest

from .base import TestBaseClass


class TestClassOelintVarsFileSettingsHidden(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.filessetting.hidden'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input',
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
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SPLITPKGS = "${PN}-ping ${PN}-arping ${PN}-tracepath ${PN}-clockdiff \
                                                 ${PN}-tftpd ${PN}-rdisc \
                                                 ${@bb.utils.contains('PACKAGECONFIG', 'rarpd', '${PN}-rarpd', '', d)} \
                                                 ${@bb.utils.contains('DISTRO_FEATURES', 'ipv6', '${PN}-traceroute6 ${PN}-ninfod', '', d)}"
                                     PACKAGES += "${SPLITPKGS}"
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
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.filessetting.hidden'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input',
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
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
