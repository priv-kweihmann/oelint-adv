from argparse import ArgumentTypeError
import argparse
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassIntegration(TestBaseClass):

    @pytest.mark.parametrize('input', 
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            INSANE_SKIP_${PN} = "foo"
            '''
            }
        ],
    )
    def test_color(self, input):
        from oelint_adv.__main__ import run
        from colorama import Fore
        _args = self._create_args(input, extraopts=["--color"])
        issues = [x[1] for x in run(_args)]
        assert(any(Fore.RED in x for x in issues)), '{} expected in:\n{}'.format("red", '\n'.join(issues))
        assert(any(Fore.YELLOW in x for x in issues)), '{} expected in:\n{}'.format("yellow", '\n'.join(issues))
        assert(any(Fore.GREEN in x for x in issues)), '{} expected in:\n{}'.format("green", '\n'.join(issues))

    def test_missing_file_args(self):
        with pytest.raises(argparse.ArgumentTypeError):
            _args = self._create_args({})

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            '''
            }
        ],
    )
    def test_constmod_add(self, input):
        from oelint_adv.__main__ import run
        from oelint_parser.constants import CONSTANTS
        __cnt = """
        {
            "functions": {
                "known": [
                    "do_foo_bar"
                ]
            }
        }
        """
        _extra_opts = ["--constantmod=+{}".format(self._create_tempfile('constmod', __cnt))]
        _args = self._create_args(input, extraopts=_extra_opts)

        assert("do_foo_bar" in CONSTANTS.FunctionsKnown)


    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            '''
            }
        ],
    )
    def test_constmod_remove(self, input):
        from oelint_adv.__main__ import run
        from oelint_parser.constants import CONSTANTS
        __cnt = """
        {
            "functions": {
                "known": [
                    "do_ar_patched"
                ]
            }
        }
        """
        _extra_opts = ["--constantmod=-{}".format(self._create_tempfile('constmod', __cnt))]
        _args = self._create_args(input, extraopts=_extra_opts)

        assert("do_ar_patched" not in CONSTANTS.FunctionsKnown)

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            '''
            }
        ],
    )
    def test_constmod_override(self, input):
        from oelint_adv.__main__ import run
        from oelint_parser.constants import CONSTANTS
        __cnt = """
        {
            "functions": {
                "known": [
                    "do_ar_patched"
                ]
            }
        }
        """
        _extra_opts = ["--constantmod={}".format(self._create_tempfile('constmod', __cnt))]
        _args = self._create_args(input, extraopts=_extra_opts)

        assert(["do_ar_patched"] == CONSTANTS.FunctionsKnown)

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            '''
            }
        ],
    )
    def test_constmod_corrupt(self, input):
        from oelint_adv.__main__ import run
        from oelint_parser.constants import CONSTANTS
        __cnt = """
        {
            "functions": 
                "known": [
                    "do_ar_patched"
                ]
            }
        }
        """
        _extra_opts = ["--constantmod={}".format(self._create_tempfile('constmod', __cnt))]
        with pytest.raises(argparse.ArgumentTypeError):
            _args = self._create_args(input, extraopts=_extra_opts)

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            '''
            }
        ],
    )
    def test_rulefile_and_subrules(self, input):
        from oelint_adv.__main__ import run
        from oelint_parser.constants import CONSTANTS
        __cnt = """
        {
            "oelint.var.suggestedvar": "info",
            "oelint.var.suggestedvar.AUTHOR": "error",
            "oelint.var.suggestedvar.BBCLASSEXTEND": "error",
            "oelint.var.suggestedvar.BUGTRACKER": "error",
            "oelint.var.suggestedvar.SECTION": "error",
            "oelint.var.suggestedvar.CVE_PRODUCT": "info"
        }
        """
        _extra_opts = ["--rulefile={}".format(self._create_tempfile('rulefile', __cnt)), '--noinfo']
        self.check_for_id(self._create_args(input, _extra_opts), 'oelint.var.suggestedvar.CVE_PRODUCT', 0)
        self.check_for_id(self._create_args(input, _extra_opts), 'oelint.var.suggestedvar.BBCLASSEXTEND', 1)

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            '''
            }
        ],
    )
    def test_rulefile_default_severity(self, input):
        from oelint_adv.__main__ import run
        _rule_file = self._create_tempfile('rulefile', '{"oelint.var.mandatoryvar": ""}')
        _args = self._create_args(input, extraopts=[f"--rulefile={_rule_file}"])
        for issue in [x[1] for x in run(_args)]:
            assert ":error:" in issue

    @pytest.mark.parametrize('id', ['oelint.var.override'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
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
            '''
            A = "1"
            ''',
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
    def test_grouping(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.var.override'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
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
            '''
            A = "1"
            ''',
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
    def test_grouping_with_missing_files(self, input, id, occurance):
        self.check_for_id(self._create_args(input, extraopts=["/does/not/exist"]), id, occurance)

    @pytest.mark.parametrize('input', 
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            INSANE_SKIP_${PN} = "foo"
            '''
            }
        ],
    )
    def test_noinfo(self, input):
        from oelint_adv.__main__ import run
        _args = self._create_args(input, extraopts=["--noinfo"])
        issues = [x[1] for x in run(_args)]
        assert(not any([x for x in issues if ':info:' in x]))

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            INSANE_SKIP_${PN} = "foo"
            '''
            }
        ],
    )
    def test_nowarn(self, input):
        from oelint_adv.__main__ import run
        _args = self._create_args(input, extraopts=["--nowarn"])
        issues = [x[1] for x in run(_args)]
        assert(not any([x for x in issues if ':warning:' in x]))

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            INSANE_SKIP_${PN} = "foo"
            '''
            }
        ],
    )
    def test_constantfile(self, input):
        from oelint_adv.__main__ import run

        _cstfile = self._create_tempfile('constants.json', '{}')

        _args = self._create_args(input, extraopts=["--constantfile={}".format(_cstfile)])
        issues = [x[1] for x in run(_args)]
        assert(any(issues))

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            INSANE_SKIP_${PN} = "foo"
            '''
            }
        ],
    )
    def test_rulefile(self, input):
        from oelint_adv.__main__ import run

        _cstfile = self._create_tempfile('constants.json', '{}')

        _args = self._create_args(input, extraopts=["--rulefile={}".format(_cstfile)])
        issues = [x[1] for x in run(_args)]
        assert(any(issues))

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            DESCRIPTION = "foo"
            '''
            }
        ],
    )
    def test_rulefile_filtering(self, input):
        from oelint_adv.__main__ import run

        _cstfile = self._create_tempfile('constants.json', '{"oelint.var.mandatoryvar.DESCRIPTION": "warning", "oelint.var.mandatoryvar": "info" }')

        _args = self._create_args(input, extraopts=["--rulefile={}".format(_cstfile), "--noinfo"])
        issues = [x[1] for x in run(_args)]
        assert(not any(issues))

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            DESCRIPTION = "foo"
            '''
            }
        ],
    )
    def test_rulefile_filtering2(self, input):
        from oelint_adv.__main__ import run

        _cstfile = self._create_tempfile('constants.json', '{"oelint.var.mandatoryvar.DESCRIPTION": "warning"}')

        _args = self._create_args(input, extraopts=["--rulefile={}".format(_cstfile)])
        issues = [x[1] for x in run(_args)]
        assert(not any(issues))

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            HOMEPAGE = "foo"
            '''
            }
        ],
    )
    def test_rulefile_filtering_invert(self, input):
        from oelint_adv.__main__ import run

        _cstfile = self._create_tempfile('constants.json', '{"oelint.var.mandatoryvar.DESCRIPTION": "warning", "oelint.var.mandatoryvar": "info" }')

        _args = self._create_args(input, extraopts=["--rulefile={}".format(_cstfile), "--noinfo"])
        issues = [x[1] for x in run(_args)]
        assert(any(issues))
        
    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            INSANE_SKIP_${PN} = "foo"
            '''
            }
        ],
    )
    def test_broken_rulefile(self, input):
        with pytest.raises(ArgumentTypeError):
            _args = self._create_args(input, extraopts=["--rulefile=/does/not/exist"])

    @pytest.mark.parametrize('input',
        [
            {"oelint.var.mandatoryvar.DESCRIPTION": "warning"},
            {"oelint.var.mandatoryvar": "warning"},
            {"oelint.var.mandatoryvar": "warning", "oelint.var.mandatoryvar.DESCRIPTION": "info"},
        ],
    )
    def test_print_rulefile(self, capsys, input):
        from oelint_adv.__main__ import print_rulefile
        import json

        _rule_file = self._create_tempfile('rules.json', json.dumps(input))
        _args = self._create_args({}, extraopts=[f"--rulefile={_rule_file}", "--print-rulefile"])
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)
        for k, v in input.items():
            assert out[k] == v

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            INSANE_SKIP_${PN} = "foo"
            '''
            }
        ],
    )
    def test_broken_constantfile(self, input):
        with pytest.raises(ArgumentTypeError):
            _args = self._create_args(input, extraopts=["--constantfile=/does/not/exist"])

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            INSANE_SKIP_${PN} = "foo"
            '''
            }
        ],
    )
    def test_nonquiet(self, input):
        from oelint_adv.__main__ import run
        from oelint_adv.__main__ import arguments_post
        _args = arguments_post(self._create_args_parser().parse_args(
            [self._create_tempfile(k, v) for k, v in input.items()]
        ))
        issues = [x[1] for x in run(_args)]
        assert(any(issues))

    def test_invalidfile(self):
        from oelint_adv.__main__ import run
        from oelint_adv.__main__ import arguments_post
        _args = arguments_post(self._create_args_parser().parse_args(
            ["/does/not/exist"]
        ))
        issues = [x[1] for x in run(_args)]
        assert(not any(issues))

    @pytest.mark.parametrize('input',
        [
            {
            'oelint adv-test.bb':
            '''
            VAR = "1"
            INSANE_SKIP_${PN} = "foo"
            '''
            }
        ],
    )
    def test_exit_zero(self, input):
        _args = self._create_args(input, extraopts=["--exit-zero"])
        assert(_args.exit_zero)