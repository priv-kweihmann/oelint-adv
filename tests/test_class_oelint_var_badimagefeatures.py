import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarLicenseRemoteFile(TestBaseClass):

    def _generate_code(self, var, feature, suffix=''):
        return {'oelint_test.bb': f'{var}{suffix} = "{feature}"'}

    @pytest.mark.parametrize('id_', ['oelint.var.badimagefeature'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', ["IMAGE_FEATURES", "EXTRA_IMAGE_FEATURES"])
    @pytest.mark.parametrize('feature', ['allow-empty-password',
                                         'allow-root-login',
                                         'dbg-pkgs',
                                         'debug-tweaks',
                                         'dev-pkgs',
                                         'eclipse-debug',
                                         'empty-root-password',
                                         'post-install-logging',
                                         'ptest-pkgs',
                                         'serial-autologin-root',
                                         'staticdev-pkgs',
                                         'tools-debug'])
    def test_bad(self, var, feature, id_, occurrence):
        self.check_for_id(self._create_args(self._generate_code(var, feature)), f'{id_}.{feature}', occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.badimagefeature'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', ["IMAGE_FEATURES", "EXTRA_IMAGE_FEATURES"])
    @pytest.mark.parametrize('feature', ['weston',
                                         'x11',
                                         'x11-base',
                                         'x11-sato',
                                         'tools-profile',
                                         'tools-testapps',
                                         'tools-sdk',
                                         'nfs-server',
                                         'nfs-client',
                                         'ssh-server-dropbear',
                                         'ssh-server-openssh',
                                         'hwcodecs',
                                         'package-management',
                                         'lic-pkgs',
                                         'doc-pkgs',
                                         'bash-completion-pkgs',
                                         'read-only-rootfs',
                                         'stateless-rootfs',
                                         'splash'])
    def test_good(self, var, feature, id_, occurrence):
        self.check_for_id(self._create_args(self._generate_code(var, feature)), f'{id_}.{feature}', occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.badimagefeature'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', ["IMAGE_FEATURES", "EXTRA_IMAGE_FEATURES"])
    @pytest.mark.parametrize('feature', ['allow-empty-password',
                                         'allow-root-login',
                                         'dbg-pkgs',
                                         'debug-tweaks',
                                         'dev-pkgs',
                                         'eclipse-debug',
                                         'empty-root-password',
                                         'post-install-logging',
                                         'ptest-pkgs',
                                         'serial-autologin-root',
                                         'staticdev-pkgs',
                                         'tools-debug'])
    def test_good_remove(self, var, feature, id_, occurrence):
        self.check_for_id(self._create_args(self._generate_code(
            var, feature, suffix=':remove')), f'{id_}.{feature}', occurrence)
