import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsDistroConf(TestBaseClass):

    def __generate_sample_code(self, var, operation):
        return '''
            {var} {operation} "foo"
            '''.format(var=var, operation=operation)

    @pytest.mark.parametrize('id_', ['oelint.vars.distroconf'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'MACHINE',
        'MACHINE_ARCH',
        'MACHINE_ESSENTIAL_EXTRA_RDEPENDS',
        'MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS',
        'MACHINE_EXTRA_RRECOMMENDS',
        'MACHINE_FEATURES',
        'MACHINE_FEATURES_BACKFILL',
        'MACHINE_FEATURES_BACKFILL_CONSIDERED',
        'IMAGE_INSTALL',
        'MACHINEOVERRIDES',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', '.=', '=.', '+=', '=+', ' =+'])
    def test_bad(self, id_, var, operation, occurrence):
        input_ = {
            'conf/distro/my.conf': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_, ['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.distroconf'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'SOME_OTHER_VAR',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', '.=', '=.', '+=', '=+', ' =+'])
    def test_good_unknown_vars(self, id_, var, operation, occurrence):
        input_ = {
            'conf/distro/my.conf': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_, ['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.distroconf'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'MACHINE',
        'MACHINE_ARCH',
        'MACHINE_ESSENTIAL_EXTRA_RDEPENDS',
        'MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS',
        'MACHINE_EXTRA_RRECOMMENDS',
        'MACHINE_FEATURES',
        'MACHINE_FEATURES_BACKFILL',
        'MACHINE_FEATURES_BACKFILL_CONSIDERED',
        'IMAGE_INSTALL',
        'MACHINEOVERRIDES',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', '.=', '=.', '+=', '=+', ' =+'])
    def test_good(self, id_, var, operation, occurrence):
        input_ = {
            'oelint-test_1.0.bb': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_, ['--mode=all']), id_, occurrence)
