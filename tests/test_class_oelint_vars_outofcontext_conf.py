import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsOutOfContextConf(TestBaseClass):

    def __generate_sample_code(self, var):
        return '''
            {var} = "foo"
            '''.format(var=var)

    @pytest.mark.parametrize('id_', ['oelint.vars.outofcontext'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        "DISTROOVERRIDES",
        "DISTRO_EXTRA_RDEPENDS",
        "DISTRO_EXTRA_RRECOMMENDS",
        "DISTRO_FEATURES",
        "DISTRO_FEATURES_BACKFILL",
        "DISTRO_FEATURES_BACKFILL_CONSIDERED",
        "DISTRO_FEATURES_DEFAULT",
        "MACHINE",
        "MACHINEOVERRIDES",
        "MACHINE_ESSENTIAL_EXTRA_RDEPENDS",
        "MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS",
        "MACHINE_EXTRA_RRECOMMENDS",
        "MACHINE_FEATURES",
        "MACHINE_FEATURES_BACKFILL",
    ])
    @pytest.mark.parametrize('filename', [
        'test_.bb',
        'test_%.bbappend',
        'classes/test.bbclass',
    ])
    def test_bad(self, id_, var, filename, occurrence):
        input_ = {
            filename: self.__generate_sample_code(var),
        }
        self.check_for_id(self._create_args(input_, extraopts=['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.outofcontext'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        "DISTROOVERRIDES",
        "DISTRO_EXTRA_RDEPENDS",
        "DISTRO_EXTRA_RRECOMMENDS",
        "DISTRO_FEATURES",
        "DISTRO_FEATURES_BACKFILL",
        "DISTRO_FEATURES_BACKFILL_CONSIDERED",
        "DISTRO_FEATURES_DEFAULT",
        "MACHINE",
        "MACHINEOVERRIDES",
        "MACHINE_ESSENTIAL_EXTRA_RDEPENDS",
        "MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS",
        "MACHINE_EXTRA_RRECOMMENDS",
        "MACHINE_FEATURES",
        "MACHINE_FEATURES_BACKFILL",
    ])
    @pytest.mark.parametrize('filename', [
        'conf/machine/test.conf',
        'conf/layer.conf',
        'conf/distro/test.conf',
    ])
    def test_good(self, id_, var, filename, occurrence):
        input_ = {
            filename: self.__generate_sample_code(var),
        }
        self.check_for_id(self._create_args(input_, extraopts=['--mode=all']), id_, occurrence)
