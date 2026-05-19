import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsMachineOptOut(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.machinefeatureoptout'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'MACHINE_FEATURES:remove = "a"',
        'MACHINE_FEATURES:remove = "a b c"',
        'MACHINE_FEATURES:remove = "x"',
    ])
    def test_bad_new(self, id_, var, occurrence):
        input_ = {
            'conf/machine/my.conf': f'{var}',
        }
        self.check_for_id(self._create_args(
            input_, ['--mode=all', '--release=wrynose']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.machinefeatureoptout'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'MACHINE_FEATURES:remove = "a"',
        'MACHINE_FEATURES:remove = "a b c"',
        'MACHINE_FEATURES:remove = "x"',
    ])
    def test_bad_old(self, id_, var, occurrence):
        input_ = {
            'conf/machine/my.conf': f'{var}',
        }
        self.check_for_id(self._create_args(
            input_, ['--mode=all', '--release=scarthgap']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.machinefeatureoptout'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'MACHINE_FEATURES:append = " a"',
        'MACHINE_FEATURES = "a b c"',
        'MACHINE_FEATURES += "a b c"',
        'MACHINE_FEATURES:prepend = "a b c "',
        'MACHINE_FEATURES_OPTED_OUT:remove = "x"',
        'MACHINE_FEATURES_OPTED_OUT:append = "x"',
        'MACHINE_FEATURES_OPTED_OUT += "x"',
    ])
    def test_good_new(self, id_, var, occurrence):
        input_ = {
            'conf/machine/my.conf': f'{var}',
        }
        self.check_for_id(self._create_args(
            input_, ['--mode=all', '--release=wrynose']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.machinefeatureoptout'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'MACHINE_FEATURES:append = " a"',
        'MACHINE_FEATURES = "a b c"',
        'MACHINE_FEATURES += "a b c"',
        'MACHINE_FEATURES:prepend = "a b c "',
        'MACHINE_FEATURES_OPTED_OUT:remove = "x"',
        'MACHINE_FEATURES_OPTED_OUT:append = "x"',
        'MACHINE_FEATURES_OPTED_OUT += "x"',
    ])
    def test_good_old(self, id_, var, occurrence):
        input_ = {
            'conf/machine/my.conf': f'{var}',
        }
        self.check_for_id(self._create_args(
            input_, ['--mode=all', '--release=scarthgap']), id_, occurrence)
