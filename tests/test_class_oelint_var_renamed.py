import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsRenamed(TestBaseClass):

    def _generate_code(self, var):
        return {'oelint_test.bb': f'{var} = "1"'}

    @pytest.mark.parametrize('id_', ['oelint.vars.renamed'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', ['PNBLACKLIST',
                                     'CVE_CHECK_PN_WHITELIST',
                                     'CVE_CHECK_WHITELIST',
                                     'MULTI_PROVIDER_WHITELIST',
                                     'SDK_LOCAL_CONF_BLACKLIST',
                                     'SDK_LOCAL_CONF_WHITELIST',
                                     'SDK_INHERIT_BLACKLIST',
                                     'SSTATE_DUPWHITELIST',
                                     'SYSROOT_DIRS_BLACKLIST',
                                     'UNKNOWN_CONFIGURE_WHITELIST',
                                     'ICECC_USER_CLASS_BL',
                                     'ICECC_SYSTEM_CLASS_BL',
                                     'ICECC_USER_PACKAGE_WL',
                                     'ICECC_USER_PACKAGE_BL',
                                     'ICECC_SYSTEM_PACKAGE_BL',
                                     'INHERIT_BLACKLIST',
                                     'TUNEABI_WHITELIST',
                                     'LICENSE_FLAGS_WHITELIST',
                                     'TCLIBCAPPEND',
                                     'VOLATILE_LOG_DIR',
                                     'VOLATILE_TMP_DIR',
                                     'WHITELIST_GPL-3.0-only',
                                     'WHITELIST_GPL-3.0-or-later',
                                     'WHITELIST_LGPL-3.0-only',
                                     'WHITELIST_LGPL-3.0-or-later'])
    def test_bad(self, var, id_, occurrence):
        self.check_for_id(self._create_args(self._generate_code(var)), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.renamed'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', ['PNBLACKLIST',
                                     'CVE_CHECK_PN_WHITELIST',
                                     'CVE_CHECK_WHITELIST',
                                     'MULTI_PROVIDER_WHITELIST',
                                     'SDK_LOCAL_CONF_BLACKLIST',
                                     'SDK_LOCAL_CONF_WHITELIST',
                                     'SDK_INHERIT_BLACKLIST',
                                     'SSTATE_DUPWHITELIST',
                                     'SYSROOT_DIRS_BLACKLIST',
                                     'UNKNOWN_CONFIGURE_WHITELIST',
                                     'ICECC_USER_CLASS_BL',
                                     'ICECC_SYSTEM_CLASS_BL',
                                     'ICECC_USER_PACKAGE_WL',
                                     'ICECC_USER_PACKAGE_BL',
                                     'ICECC_SYSTEM_PACKAGE_BL',
                                     'INHERIT_BLACKLIST',
                                     'TUNEABI_WHITELIST',
                                     'LICENSE_FLAGS_WHITELIST',
                                     'TCLIBCAPPEND',
                                     'VOLATILE_LOG_DIR',
                                     'VOLATILE_TMP_DIR',
                                     'WHITELIST_GPL-3.0-only',
                                     'WHITELIST_GPL-3.0-or-later',
                                     'WHITELIST_LGPL-3.0-only',
                                     'WHITELIST_LGPL-3.0-or-later'])
    def test_bad_older_release(self, var, id_, occurrence):
        self.check_for_id(self._create_args(self._generate_code(var), ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.renamed'])
    @pytest.mark.parametrize('var', ['PNBLACKLIST',
                                     'CVE_CHECK_PN_WHITELIST',
                                     'CVE_CHECK_WHITELIST',
                                     'MULTI_PROVIDER_WHITELIST',
                                     'SDK_LOCAL_CONF_BLACKLIST',
                                     'SDK_LOCAL_CONF_WHITELIST',
                                     'SDK_INHERIT_BLACKLIST',
                                     'SSTATE_DUPWHITELIST',
                                     'SYSROOT_DIRS_BLACKLIST',
                                     'UNKNOWN_CONFIGURE_WHITELIST',
                                     'ICECC_USER_CLASS_BL',
                                     'ICECC_SYSTEM_CLASS_BL',
                                     'ICECC_USER_PACKAGE_WL',
                                     'ICECC_USER_PACKAGE_BL',
                                     'ICECC_SYSTEM_PACKAGE_BL',
                                     'LICENSE_FLAGS_WHITELIST',
                                     'WHITELIST_GPL-3.0-only',
                                     'WHITELIST_GPL-3.0-or-later',
                                     'WHITELIST_LGPL-3.0-only',
                                     'WHITELIST_LGPL-3.0-or-later'])
    def test_fix(self, var, id_):
        self.fix_and_check(self._create_args_fix(self._generate_code(var)), id_)

    @pytest.mark.parametrize('id_', ['oelint.vars.renamed'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', ['INHERIT_BLACKLIST',
                                     'TUNEABI_WHITELIST',
                                     'TCLIBCAPPEND',
                                     'VOLATILE_LOG_DIR',
                                     'VOLATILE_TMP_DIR'])
    def test_bad_unfixable(self, var, id_, occurrence):
        self.check_for_id(self._create_args_fix(self._generate_code(var)), id_, occurrence)
