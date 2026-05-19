import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsDistroConf(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.distrofeatureoptout'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'DISTRO_FEATURES:remove = "a"',
        'DISTRO_FEATURES:remove = "a b c"',
        'DISTRO_FEATURES:remove = "x"',
    ])
    def test_bad_new(self, id_, var, occurrence):
        input_ = {
            'conf/distro/my.conf': f'{var}',
        }
        self.check_for_id(self._create_args(
            input_, ['--mode=all', '--release=wrynose']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.distrofeatureoptout'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'DISTRO_FEATURES:remove = "a"',
        'DISTRO_FEATURES:remove = "a b c"',
        'DISTRO_FEATURES:remove = "x"',
    ])
    def test_bad_old(self, id_, var, occurrence):
        input_ = {
            'conf/distro/my.conf': f'{var}',
        }
        self.check_for_id(self._create_args(
            input_, ['--mode=all', '--release=scarthgap']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.distrofeatureoptout'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'DISTRO_FEATURES:append = " a"',
        'DISTRO_FEATURES = "a b c"',
        'DISTRO_FEATURES += "a b c"',
        'DISTRO_FEATURES:prepend = "a b c "',
        'DISTRO_FEATURES_OPTED_OUT:remove = "x"',
        'DISTRO_FEATURES_OPTED_OUT:append = "x"',
        'DISTRO_FEATURES_OPTED_OUT += "x"',
    ])
    def test_good_new(self, id_, var, occurrence):
        input_ = {
            'conf/distro/my.conf': f'{var}',
        }
        self.check_for_id(self._create_args(
            input_, ['--mode=all', '--release=wrynose']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.distrofeatureoptout'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'DISTRO_FEATURES:append = " a"',
        'DISTRO_FEATURES = "a b c"',
        'DISTRO_FEATURES += "a b c"',
        'DISTRO_FEATURES:prepend = "a b c "',
        'DISTRO_FEATURES_OPTED_OUT:remove = "x"',
        'DISTRO_FEATURES_OPTED_OUT:append = "x"',
        'DISTRO_FEATURES_OPTED_OUT += "x"',
    ])
    def test_good_old(self, id_, var, occurrence):
        input_ = {
            'conf/distro/my.conf': f'{var}',
        }
        self.check_for_id(self._create_args(
            input_, ['--mode=all', '--release=scarthgap']), id_, occurrence)
