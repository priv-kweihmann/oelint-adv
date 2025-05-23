import argparse
import json
import os
from argparse import ArgumentTypeError

import pytest  # noqa: I900

from .base import TestBaseClass


# flake8: noqa S101 - n.a. for test files
class TestClassIntegration(TestBaseClass):

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_color_input(self, input_):
        # local imports only
        from colorama import Fore
        from oelint_adv.__main__ import run

        _args = self._create_args(input_, extraopts=['--color'])
        issues = [x[1] for x in run(_args)]
        issues_formatted = '\n'.join(issues)
        assert (any(Fore.RED in x for x in issues)
                ), f'red expected in:\n{issues_formatted}'
        assert (any(Fore.YELLOW in x for x in issues)
                ), f'yellow expected in:\n{issues_formatted}'
        assert (any(Fore.GREEN in x for x in issues)
                ), f'green expected in:\n{issues_formatted}'

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_relpaths(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(input_, extraopts=['--relpaths'])
        _cwd = os.getcwd()
        os.chdir('/tmp')  # noqa: S108 - usage of tmp is fine for our purposes
        issues = [x[1] for x in run(_args)]
        assert (not any(x.startswith('/tmp/') for x in issues))  # noqa: S108 - usage of tmp is fine for our purposes
        os.chdir(_cwd)

    def test_missing_file_args(self):
        with pytest.raises(ArgumentTypeError):
            self._create_args({})

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     'VAR = "1"',
                                 },
                             ],
                             )
    def test_constmod_add(self, input_):
        # local imports only
        from oelint_parser.constants import CONSTANTS

        __cnt = '''
        {
            "functions": {
                "known": [
                    "do_foo_bar"
                ]
            }
        }
        '''
        _extra_opts = [
            '--constantmod=+{mod}'.format(mod=self._create_tempfile('constmod', __cnt))]
        _args = self._create_args(input_, extraopts=_extra_opts)

        assert ('do_foo_bar' in CONSTANTS.FunctionsKnown)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     'VAR = "1"',
                                 },
                             ],
                             )
    def test_constmod_remove(self, input_):
        # local imports only
        from oelint_parser.constants import CONSTANTS

        __cnt = '''
        {
            "functions": {
                "known": [
                    "do_ar_patched"
                ]
            }
        }
        '''
        _extra_opts = [
            '--constantmod=-{mod}'.format(mod=self._create_tempfile('constmod', __cnt))]
        self._create_args(input_, extraopts=_extra_opts)

        assert ('do_ar_patched' not in CONSTANTS.FunctionsKnown)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     'VAR = "1"',
                                 },
                             ],
                             )
    def test_constmod_override(self, input_):
        # local imports only
        from oelint_parser.constants import CONSTANTS

        __cnt = '''
        {
            "functions": {
                "known": [
                    "do_ar_patched"
                ]
            }
        }
        '''
        _extra_opts = [
            '--constantmod={mod}'.format(mod=self._create_tempfile('constmod', __cnt))]
        _args = self._create_args(input_, extraopts=_extra_opts)

        assert (['do_ar_patched'] == CONSTANTS.FunctionsKnown)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     'VAR = "1"',
                                 },
                             ],
                             )
    def test_constmod_corrupt(self, input_):
        __cnt = '''
        {
            "functions": 
                "known": [
                    "do_ar_patched"
                ]
            }
        }
        '''
        _extra_opts = [
            '--constantmod={}'.format(self._create_tempfile('constmod', __cnt))]
        with pytest.raises(ArgumentTypeError):
            self._create_args(input_, extraopts=_extra_opts)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     'VAR = "1"',
                                 },
                             ],
                             )
    def test_rulefile_and_subrules(self, input_):
        __cnt = '''
        {
            "oelint.var.suggestedvar": "info",
            "oelint.var.suggestedvar.AUTHOR": "error",
            "oelint.var.suggestedvar.BBCLASSEXTEND": "error",
            "oelint.var.suggestedvar.BUGTRACKER": "error",
            "oelint.var.suggestedvar.SECTION": "error",
            "oelint.var.suggestedvar.CVE_PRODUCT": "info"
        }
        '''
        _extra_opts = [
            '--rulefile={file}'.format(file=self._create_tempfile('rulefile', __cnt)), '--hide', 'info']
        self.check_for_id(self._create_args(input_, _extra_opts),
                          'oelint.var.suggestedvar.CVE_PRODUCT', 0)

    def test_rulefile_subrules_printout(self, capsys):
        from oelint_adv.__main__ import print_rulefile
        __cnt = {
            "oelint.var.suggestedvar.BUGTRACKER": "error",
        }
        _extra_opts = ['--rulefile={file}'.format(file=self._create_tempfile('rulefile', json.dumps(__cnt)))]

        print_rulefile(self._create_args_plain(['--print-rulefile'], _extra_opts))
        captured = capsys.readouterr()
        assert json.loads(captured.out) == __cnt

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     'VAR = "1"',
                                 },
                             ],
                             )
    def test_rulefile_default_severity(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _rule_file = self._create_tempfile(
            'rulefile', '{"oelint.var.mandatoryvar": ""}')
        _args = self._create_args(
            input_, extraopts=[f'--rulefile={_rule_file}'])
        for issue in [x[1] for x in run(_args)]:
            assert ':error:' in issue

    @pytest.mark.parametrize('id_', ['oelint.var.override'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'optee-client_3.11.0.bb':
                                     '''
                                     require optee-client.inc
                                     SRCREV = "c0c925384c1d7e3558d27d2708857482952d7907"
                                     ''',
                                     'optee-client.inc':
                                     '''
                                     SUMMARY = "OP-TEE Client API"
                                     DESCRIPTION = "Open Portable Trusted Execution Environment - Normal World Client side of the TEE"
                                     HOMEPAGE = "https://www.op-tee.org/"
                                     LICENSE = "BSD-2-Clause"
                                     LIC_FILES_CHKSUM = "file://LICENSE;md5=69663ab153298557a59c67a60a743e5b"
                                     inherit systemd update-rc.d cmake
                                     SRC_URI = " \\
                                         git://github.com/OP-TEE/optee_client.git \\
                                         file://tee-supplicant.service \\
                                         file://tee-supplicant.sh \\
                                     "
                                     S = "${WORKDIR}/git"
                                     EXTRA_OECMAKE = " \\
                                         -DBUILD_SHARED_LIBS=ON \\
                                         -DCFG_TEE_FS_PARENT_PATH='${localstatedir}/lib/tee' \\
                                     "
                                     EXTRA_OECMAKE_append_toolchain-clang = " -DCFG_WERROR=0"
                                     do_install_append() {
                                         install -D -p -m0644 ${WORKDIR}/tee-supplicant.service ${D}${systemd_system_unitdir}/tee-supplicant.service
                                         install -D -p -m0755 ${WORKDIR}/tee-supplicant.sh ${D}${sysconfdir}/init.d/tee-supplicant
                                         sed -i -e s:@sysconfdir@:${sysconfdir}:g \\
                                             -e s:@sbindir@:${sbindir}:g \\
                                                 ${D}${systemd_system_unitdir}/tee-supplicant.service \\
                                                 ${D}${sysconfdir}/init.d/tee-supplicant
                                     }
                                     SYSTEMD_SERVICE_${PN} = "tee-supplicant.service"
                                     INITSCRIPT_PACKAGES = "${PN}"
                                     INITSCRIPT_NAME_${PN} = "tee-supplicant"
                                     INITSCRIPT_PARAMS_${PN} = "start 10 1 2 3 4 5 . stop 90 0 6 ."
                                     ''',
                                     'optee-examples_3.11.0.bb':
                                     '''
                                     require optee-examples.inc
                                     SRCREV = "9a7dc598591990349d88b4dba3a37aadd6851295"
                                     ''',
                                     'optee-examples_%.bbappend':
                                     'A = "1"',
                                     'optee-examples.inc':
                                     '''
                                     SUMMARY = "OP-TEE examples"
                                     DESCRIPTION = "Open Portable Trusted Execution Environment - Sample Applications"
                                     HOMEPAGE = "https://github.com/linaro-swg/optee_examples"
                                     LICENSE = "BSD-2-Clause"
                                     LIC_FILES_CHKSUM = "file://LICENSE;md5=cd95ab417e23b94f381dafc453d70c30"
                                     DEPENDS = "optee-client optee-os python3-pycryptodome-native"
                                     inherit python3native
                                     require optee.inc
                                     SRC_URI = "git://github.com/linaro-swg/optee_examples.git \\
                                             file://0001-make-Pass-ldflags-during-link.patch \\
                                             "
                                     EXTRA_OEMAKE += "TA_DEV_KIT_DIR=${TA_DEV_KIT_DIR} \\
                                                     HOST_CROSS_COMPILE=${HOST_PREFIX} \\
                                                     TA_CROSS_COMPILE=${HOST_PREFIX} \\
                                                     OUTPUT_DIR=${B} \\
                                                 "
                                     S = "${WORKDIR}/git"
                                     B = "${WORKDIR}/build"
                                     do_compile() {
                                         oe_runmake -C ${S}
                                     }
                                     do_compile[cleandirs] = "${B}"
                                     do_install () {
                                         mkdir -p ${D}${nonarch_base_libdir}/optee_armtz
                                         mkdir -p ${D}${bindir}
                                         install -D -p -m0755 ${B}/ca/* ${D}${bindir}
                                         install -D -p -m0444 ${B}/ta/* ${D}${nonarch_base_libdir}/optee_armtz
                                     }
                                     FILES_${PN} += "${nonarch_base_libdir}/optee_armtz/"
                                     # Imports machine specific configs from staging to build
                                     PACKAGE_ARCH = "${MACHINE_ARCH}"
                                     ''',
                                     'optee.inc':
                                     '''
                                     COMPATIBLE_MACHINE ?= "invalid"
                                     COMPATIBLE_MACHINE_qemuarm64 ?= "qemuarm64"
                                     # Please add supported machines below or set it in .bbappend or .conf
                                     OPTEEMACHINE ?= "${MACHINE}"
                                     OPTEEMACHINE_aarch64_qemuall ?= "vexpress-qemu_armv8a"
                                     OPTEE_ARCH = "null"
                                     OPTEE_ARCH_armv7a = "arm32"
                                     OPTEE_ARCH_aarch64 = "arm64"
                                     OPTEE_CORE = "${@d.getVar('OPTEE_ARCH').upper()}"
                                     OPTEE_TOOLCHAIN = "${@d.getVar('TOOLCHAIN') or 'gcc'}"
                                     OPTEE_COMPILER = "${@bb.utils.contains("BBFILE_COLLECTIONS", "clang-layer", "${OPTEE_TOOLCHAIN}", "gcc", d)}"
                                     # Set here but not passed to EXTRA_OEMAKE by default as that breaks
                                     # the optee-os build
                                     TA_DEV_KIT_DIR = "${STAGING_INCDIR}/optee/export-user_ta"
                                     EXTRA_OEMAKE += "V=1 \\
                                                     LIBGCC_LOCATE_CFLAGS=--sysroot=${STAGING_DIR_HOST} \\
                                                     COMPILER=${OPTEE_COMPILER} \\
                                                     OPTEE_CLIENT_EXPORT=${STAGING_DIR_HOST}${prefix} \\
                                                     TEEC_EXPORT=${STAGING_DIR_HOST}${prefix} \\
                                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_grouping(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.override'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'optee-client_3.11.0.bb':
                                     '''
                                     require optee-client.inc
                                     SRCREV = "c0c925384c1d7e3558d27d2708857482952d7907"
                                     ''',
                                     'optee-client.inc':
                                     '''
                                     SUMMARY = "OP-TEE Client API"
                                     DESCRIPTION = "Open Portable Trusted Execution Environment - Normal World Client side of the TEE"
                                     HOMEPAGE = "https://www.op-tee.org/"
                                     LICENSE = "BSD-2-Clause"
                                     LIC_FILES_CHKSUM = "file://LICENSE;md5=69663ab153298557a59c67a60a743e5b"
                                     inherit systemd update-rc.d cmake
                                     SRC_URI = " \\
                                         git://github.com/OP-TEE/optee_client.git \\
                                         file://tee-supplicant.service \\
                                         file://tee-supplicant.sh \\
                                     "
                                     S = "${WORKDIR}/git"
                                     EXTRA_OECMAKE = " \\
                                         -DBUILD_SHARED_LIBS=ON \\
                                         -DCFG_TEE_FS_PARENT_PATH='${localstatedir}/lib/tee' \\
                                     "
                                     EXTRA_OECMAKE_append_toolchain-clang = " -DCFG_WERROR=0"
                                     do_install_append() {
                                         install -D -p -m0644 ${WORKDIR}/tee-supplicant.service ${D}${systemd_system_unitdir}/tee-supplicant.service
                                         install -D -p -m0755 ${WORKDIR}/tee-supplicant.sh ${D}${sysconfdir}/init.d/tee-supplicant
                                         sed -i -e s:@sysconfdir@:${sysconfdir}:g \\
                                             -e s:@sbindir@:${sbindir}:g \\
                                                 ${D}${systemd_system_unitdir}/tee-supplicant.service \\
                                                 ${D}${sysconfdir}/init.d/tee-supplicant
                                     }
                                     SYSTEMD_SERVICE_${PN} = "tee-supplicant.service"
                                     INITSCRIPT_PACKAGES = "${PN}"
                                     INITSCRIPT_NAME_${PN} = "tee-supplicant"
                                     INITSCRIPT_PARAMS_${PN} = "start 10 1 2 3 4 5 . stop 90 0 6 ."
                                     ''',
                                     'optee-examples_3.11.0.bb':
                                     '''
                                     require optee-examples.inc
                                     SRCREV = "9a7dc598591990349d88b4dba3a37aadd6851295"
                                     ''',
                                     'optee-examples_%.bbappend':
                                     'A = "1"',
                                     'optee-examples.inc':
                                     '''
                                     SUMMARY = "OP-TEE examples"
                                     DESCRIPTION = "Open Portable Trusted Execution Environment - Sample Applications"
                                     HOMEPAGE = "https://github.com/linaro-swg/optee_examples"
                                     LICENSE = "BSD-2-Clause"
                                     LIC_FILES_CHKSUM = "file://LICENSE;md5=cd95ab417e23b94f381dafc453d70c30"
                                     DEPENDS = "optee-client optee-os python3-pycryptodome-native"
                                     inherit python3native
                                     require optee.inc
                                     SRC_URI = "git://github.com/linaro-swg/optee_examples.git \\
                                             file://0001-make-Pass-ldflags-during-link.patch \\
                                             "
                                     EXTRA_OEMAKE += "TA_DEV_KIT_DIR=${TA_DEV_KIT_DIR} \\
                                                     HOST_CROSS_COMPILE=${HOST_PREFIX} \\
                                                     TA_CROSS_COMPILE=${HOST_PREFIX} \\
                                                     OUTPUT_DIR=${B} \\
                                                 "
                                     S = "${WORKDIR}/git"
                                     B = "${WORKDIR}/build"
                                     do_compile() {
                                         oe_runmake -C ${S}
                                     }
                                     do_compile[cleandirs] = "${B}"
                                     do_install () {
                                         mkdir -p ${D}${nonarch_base_libdir}/optee_armtz
                                         mkdir -p ${D}${bindir}
                                         install -D -p -m0755 ${B}/ca/* ${D}${bindir}
                                         install -D -p -m0444 ${B}/ta/* ${D}${nonarch_base_libdir}/optee_armtz
                                     }
                                     FILES_${PN} += "${nonarch_base_libdir}/optee_armtz/"
                                     # Imports machine specific configs from staging to build
                                     PACKAGE_ARCH = "${MACHINE_ARCH}"
                                     ''',
                                     'optee.inc':
                                     '''
                                     COMPATIBLE_MACHINE ?= "invalid"
                                     COMPATIBLE_MACHINE_qemuarm64 ?= "qemuarm64"
                                     # Please add supported machines below or set it in .bbappend or .conf
                                     OPTEEMACHINE ?= "${MACHINE}"
                                     OPTEEMACHINE_aarch64_qemuall ?= "vexpress-qemu_armv8a"
                                     OPTEE_ARCH = "null"
                                     OPTEE_ARCH_armv7a = "arm32"
                                     OPTEE_ARCH_aarch64 = "arm64"
                                     OPTEE_CORE = "${@d.getVar('OPTEE_ARCH').upper()}"
                                     OPTEE_TOOLCHAIN = "${@d.getVar('TOOLCHAIN') or 'gcc'}"
                                     OPTEE_COMPILER = "${@bb.utils.contains("BBFILE_COLLECTIONS", "clang-layer", "${OPTEE_TOOLCHAIN}", "gcc", d)}"
                                     # Set here but not passed to EXTRA_OEMAKE by default as that breaks
                                     # the optee-os build
                                     TA_DEV_KIT_DIR = "${STAGING_INCDIR}/optee/export-user_ta"
                                     EXTRA_OEMAKE += "V=1 \\
                                                     LIBGCC_LOCATE_CFLAGS=--sysroot=${STAGING_DIR_HOST} \\
                                                     COMPILER=${OPTEE_COMPILER} \\
                                                     OPTEE_CLIENT_EXPORT=${STAGING_DIR_HOST}${prefix} \\
                                                     TEEC_EXPORT=${STAGING_DIR_HOST}${prefix} \\
                                                     "
                                     ''',
                                 }
                             ],
                             )
    def test_grouping_with_missing_files(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, extraopts=[
                          '/does/not/exist']), id, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.multiinclude'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'u-boot-rahix.bb':
                                     '''
                                     require u-boot-rahix-common.inc
                                     ''',
                                     'u-boot-rahix-tools.bb':
                                     '''
                                     require u-boot-rahix-common.inc
                                     ''',
                                     'u-boot-rahix-common.inc':
                                     '''
                                     require recipes-bsp/u-boot/u-boot-common.inc
                                     ''',
                                 }
                             ],
                             )
    def test_grouping_with_noversion(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.multiinclude'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'test.bb':
                                     '''
                                     require test.inc
                                     ''',
                                     'test_1.2.3.bb':
                                     '''
                                     require test.inc
                                     ''',
                                     'test_git.bb':
                                     '''
                                     require test.inc
                                     ''',
                                     'test_1.%.bbappend':
                                     '''
                                     require test2.inc
                                     ''',
                                     'test_git.bbappend':
                                     '''
                                     require test2.inc
                                     ''',
                                     'test.inc':
                                     '''
                                     A = "1"
                                     ''',
                                     'test2.inc':
                                     '''
                                     B = "1"
                                     ''',
                                 }
                             ],
                             )
    def test_grouping_with_noversion2(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_hide_info(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(input_, extraopts=['--hide', 'info'])
        issues = [x[1] for x in run(_args)]
        assert (not any([x for x in issues if ':info:' in x]))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_hide_warning(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(input_, extraopts=['--hide', 'warning'])
        issues = [x[1] for x in run(_args)]
        assert (not any([x for x in issues if ':warning:' in x]))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     FILES = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_hide_error(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(input_, extraopts=['--hide', 'error'])
        issues = [x[1] for x in run(_args)]
        assert (not any([x for x in issues if ':error:' in x]))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_noinfo(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(input_, extraopts=['--noinfo'])
        issues = [x[1] for x in run(_args)]
        assert (not any([x for x in issues if ':info:' in x]))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_nowarn(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(input_, extraopts=['--nowarn'])
        issues = [x[1] for x in run(_args)]
        assert (not any([x for x in issues if ':warning:' in x]))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 }
                             ],
                             )
    def test_messageformat_1(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(
            input_, extraopts=['--messageformat="BAR:FOO"'])
        issues = [x[1] for x in run(_args)]
        assert (any([x for x in issues if 'BAR:FOO' in x]))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP:${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_messageformat_2(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(
            input_, extraopts=['--messageformat="{id}:{severity}:{msg}"'])
        issues = [x[1] for x in run(_args)]
        assert (any([x for x in issues if 'oelint.vars.insaneskip:error:' in x]))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP:${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_messageformat_wikiurl(self, input_):
        # local imports only
        from oelint_adv.__main__ import run
        from oelint_adv.version import __version__

        _args = self._create_args(
            input_, extraopts=['--messageformat="{wikiurl}"'])
        issues = [x[1] for x in run(_args)]
        assert (any(
            [x for x in issues if f'https://github.com/priv-kweihmann/oelint-adv/blob/{__version__}/docs/wiki/oelint.vars.insaneskip.md' in x]))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP:${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_messageformat_rungroup(self, input_):
        # local imports only
        from oelint_adv.__main__ import run
        from oelint_adv.version import __version__

        _args = self._create_args(
            input_, extraopts=['--messageformat="{rungroup}"'])
        issues = [x[1] for x in run(_args)]
        assert (any(
            [x for x in issues if f'oelint adv-test.bb' in x]))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_messageformat_2_old(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(
            input_, extraopts=['--messageformat="{id}:{severity}:{msg}"', '--release=dunfell'])
        issues = [x[1] for x in run(_args)]
        assert (any([x for x in issues if 'oelint.vars.insaneskip:error:' in x]))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_rulefile(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _cstfile = self._create_tempfile('constants.json', '{}')

        _args = self._create_args(
            input_, extraopts=['--rulefile={file}'.format(file=_cstfile)])
        issues = [x[1] for x in run(_args)]
        assert (any(issues))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                    A = "1"
                                    ''',
                                 },
                             ],
                             )
    def test_rulefile_subids_only(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _rule_file = {
            "oelint.var.mandatoryvar.DESCRIPTION": "error",
            "oelint.var.mandatoryvar.LICENSE": "error",
            "oelint.var.mandatoryvar.SRC_URI": "error"
        }

        _cstfile = self._create_tempfile('rules.json', json.dumps(_rule_file))

        _args = self._create_args(
            input_, extraopts=['--rulefile={file}'.format(file=_cstfile)])
        issues = [x[1] for x in run(_args)]
        assert (not any(any(x.startswith(y) for y in _rule_file.keys()) for x in issues))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     'DESCRIPTION = "foo"',
                                 },
                             ],
                             )
    def test_rulefile_filtering(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _cstfile = self._create_tempfile(
            'constants.json', '{"oelint.var.mandatoryvar.DESCRIPTION": "warning", "oelint.var.mandatoryvar": "info" }')

        _args = self._create_args(
            input_, extraopts=['--rulefile={file}'.format(file=_cstfile), '--hide', 'info'])
        issues = [x[1] for x in run(_args)]
        assert (not any(issues))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     'DESCRIPTION = "foo"',
                                 },
                             ],
                             )
    def test_rulefile_filtering2(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _cstfile = self._create_tempfile(
            'constants.json', '{"oelint.var.mandatoryvar.DESCRIPTION": "warning"}')

        _args = self._create_args(
            input_, extraopts=['--rulefile={file}'.format(file=_cstfile)])
        issues = [x[1] for x in run(_args)]
        assert (not any("oelint.var.mandatoryvar.DESCRIPTION" in x for x in issues))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     'HOMEPAGE = "foo"',
                                 },
                             ],
                             )
    def test_rulefile_filtering_invert(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _cstfile = self._create_tempfile(
            'constants.json', '{"oelint.var.mandatoryvar.DESCRIPTION": "warning", "oelint.var.mandatoryvar": "info" }')

        _args = self._create_args(
            input_, extraopts=['--rulefile={file}'.format(file=_cstfile), '--hide', 'info'])
        issues = [x[1] for x in run(_args)]
        assert (any(issues))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_broken_rulefile(self, input_):
        with pytest.raises(ArgumentTypeError):
            _args = self._create_args(
                input_, extraopts=['--rulefile=/does/not/exist'])

    @pytest.mark.parametrize('input_',
                             [
                                 {'oelint.var.mandatoryvar.DESCRIPTION': 'warning'},
                                 {'oelint.var.mandatoryvar': 'warning'},
                                 {'oelint.var.mandatoryvar': 'warning',
                                  'oelint.var.mandatoryvar.DESCRIPTION': 'info'},
                             ],
                             )
    def test_print_rulefile(self, capsys, input_):
        # local imports only
        from oelint_adv.__main__ import print_rulefile

        _rule_file = self._create_tempfile('rules.json', json.dumps(input_))
        _args = self._create_args(
            {}, extraopts=[f'--rulefile={_rule_file}', '--print-rulefile'])
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)
        for k, v in input_.items():
            assert out[k] == v

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_nonquiet(self, input_):
        # local imports only
        from oelint_adv.__main__ import arguments_post
        from oelint_adv.__main__ import run

        _args = arguments_post(self._create_args_parser().parse_args(
            [self._create_tempfile(k, v) for k, v in input_.items()]
        ))
        issues = [x[1] for x in run(_args)]
        assert (any(issues))

    def test_invalidfile(self):
        # local imports only
        from oelint_adv.__main__ import arguments_post
        from oelint_adv.__main__ import run

        _args = arguments_post(self._create_args_parser().parse_args(
            ['/does/not/exist']
        ))
        issues = [x[1] for x in run(_args)]
        assert (not any(issues))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_exit_zero(self, input_):
        _args = self._create_args(input_, extraopts=['--exit-zero'])
        assert (_args.exit_zero)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv-test_2.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint adv-test_1.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_sorted_by_file_and_line(self, capsys, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(input_)
        issues = [x[0] for x in run(_args)]

        assert sorted(issues, key=lambda x: x[0]) == issues

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv-test_2.bb':
                                     '''
                                     VAR = "1"
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 }
                             ],
                             )
    def test_suppress(self, capsys, input_):
        _args = self._create_args(input_, ['--suppress="a b c"', '--suppress="d"'])

        assert "a" in _args.suppress
        assert "b" in _args.suppress
        assert "c" in _args.suppress
        assert "d" in _args.suppress

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     ''',
                                 }
                             ],
                             )
    def test_release_author(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(
            input_, extraopts=['--release=sumo'])
        issues = [x[1] for x in run(_args)]
        assert (any([x for x in issues if 'AUTHOR' in x]))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     ''',
                                 }
                             ],
                             )
    def test_release_no_author(self, input_):
        # local imports only
        from oelint_adv.__main__ import run

        _args = self._create_args(
            input_, extraopts=['--release=nanbield'])
        issues = [x[1] for x in run(_args)]
        assert not any([x for x in issues if 'AUTHOR' in x])

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     ''',
                                 }
                             ],
                             )
    def test_release_invalid(self, input_):
        with pytest.raises(SystemExit):
            self._create_args(input_, extraopts=['--release=doesnotexist'])

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     ''',
                                 }
                             ],
                             )
    def test_no_known_variable_file(self, input_):
        from oelint_adv.__main__ import run

        run(self._create_args(input_, extraopts=['--release=dunfell']))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     ''',
                                 }
                             ],
                             )
    def test_latest_alias(self, input_):
        from oelint_adv.__main__ import run

        run(self._create_args(input_, extraopts=['--release=latest']))

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     VAR = "1"
                                     ''',
                                 }
                             ],
                             )
    def test_fix_and_jobs(self, input_, capsys):

        args = self._create_args(input_, extraopts=['--fix', '--nobackup', '--jobs=2'])

        captured = capsys.readouterr()
        assert 'WARNING: --fix should only be run in single job mode (--jobs=1)' in captured.out
        assert args.jobs == 1

        args = self._create_args(input_, extraopts=['--fix', '--nobackup', '--jobs=1'])

        captured = capsys.readouterr()
        assert 'WARNING: --fix should only be run in single job mode (--jobs=1)' not in captured.out
        assert args.jobs == 1
