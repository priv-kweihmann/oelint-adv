import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsMachineConf(TestBaseClass):

    def __generate_sample_code(self, var, operation):
        return '''
            {var} {operation} "foo"
            '''.format(var=var, operation=operation)

    @pytest.mark.parametrize('id_', ['oelint.vars.machineconf'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'DISTROOVERRIDES',
        'DISTRO_EXTRA_RDEPENDS',
        'DISTRO_EXTRA_RRECOMMENDS',
        'DISTRO_FEATURES',
        'DISTRO_FEATURES_BACKFILL',
        'DISTRO_FEATURES_BACKFILL_CONSIDERED',
        'DISTRO_FEATURES_DEFAULT',
        'IMAGE_INSTALL',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', '.=', '=.', '+=', '=+', ' =+'])
    def test_bad(self, id_, var, operation, occurrence):
        input_ = {
            'conf/machine/mymachine.conf': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_, ['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.machineconf'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'SOME_OTHER_VAR',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', '.=', '=.', '+=', '=+', ' =+'])
    def test_good_unknown_vars(self, id_, var, operation, occurrence):
        input_ = {
            'conf/machine/mymachine.conf': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_, ['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.machineconf'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'DISTROOVERRIDES',
        'DISTRO_EXTRA_RDEPENDS',
        'DISTRO_EXTRA_RRECOMMENDS',
        'DISTRO_FEATURES',
        'DISTRO_FEATURES_BACKFILL',
        'DISTRO_FEATURES_BACKFILL_CONSIDERED',
        'DISTRO_FEATURES_DEFAULT',
        'IMAGE_INSTALL',
        'SOME_OTHER_VAR',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', '.=', '=.', '+=', '=+', ' =+'])
    def test_good(self, id_, var, operation, occurrence):
        input_ = {
            'oelint-test_1.0.bb': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_, ['--mode=all']), id_, occurrence)
