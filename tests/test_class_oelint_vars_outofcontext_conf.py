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
        "DISTRO_FEATURES_OPTED_OUT",
        "MACHINE",
        "MACHINEOVERRIDES",
        "MACHINE_ESSENTIAL_EXTRA_RDEPENDS",
        "MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS",
        "MACHINE_EXTRA_RRECOMMENDS",
        "MACHINE_FEATURES",
        "MACHINE_FEATURES_BACKFILL",
        "MACHINE_FEATURES_OPTED_OUT",
        "BBFILES",
        "BBFILES_DYNAMIC",
        "BBFILE_COLLECTIONS",
        "BBPATH",
        "HOSTTOOLS_NONFATAL",
        "LICENSE_PATH",
    ])
    @pytest.mark.parametrize('filename', [
        'test_.bb',
        'test_%.bbappend',
        'classes/test.bbclass',
    ])
    def test_bad_recipe_classes_appends(self, id_, var, filename, occurrence):
        input_ = {
            filename: self.__generate_sample_code(var),
        }
        self.check_for_id(self._create_args(
            input_, extraopts=['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.outofcontext'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        "MACHINE",
        "MACHINEOVERRIDES",
        "MACHINE_ESSENTIAL_EXTRA_RDEPENDS",
        "MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS",
        "MACHINE_EXTRA_RRECOMMENDS",
        "MACHINE_FEATURES",
        "MACHINE_FEATURES_BACKFILL",
        "MACHINE_FEATURES_OPTED_OUT",
        "BBFILES",
        "BBFILES_DYNAMIC",
        "BBFILE_COLLECTIONS",
        "BBPATH",
        "HOSTTOOLS_NONFATAL",
        "LICENSE_PATH",
    ])
    @pytest.mark.parametrize('filename', [
        'conf/distro/test.conf',
    ])
    def test_bad_distro(self, id_, var, filename, occurrence):
        input_ = {
            filename: self.__generate_sample_code(var),
        }
        self.check_for_id(self._create_args(
            input_, extraopts=['--mode=all']), id_, occurrence)

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
        "DISTRO_FEATURES_OPTED_OUT",
        "BBFILES",
        "BBFILES_DYNAMIC",
        "BBFILE_COLLECTIONS",
        "BBPATH",
        "HOSTTOOLS_NONFATAL",
        "LICENSE_PATH",
    ])
    @pytest.mark.parametrize('filename', [
        'conf/machine/test.conf',
    ])
    def test_bad_machine(self, id_, var, filename, occurrence):
        input_ = {
            filename: self.__generate_sample_code(var),
        }
        self.check_for_id(self._create_args(
            input_, extraopts=['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.outofcontext'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        "MACHINE",
        "MACHINEOVERRIDES",
        "MACHINE_ESSENTIAL_EXTRA_RDEPENDS",
        "MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS",
        "MACHINE_EXTRA_RRECOMMENDS",
        "MACHINE_FEATURES",
        "MACHINE_FEATURES_BACKFILL",
        "MACHINE_FEATURES_OPTED_OUT",
        "DISTROOVERRIDES",
        "DISTRO_EXTRA_RDEPENDS",
        "DISTRO_EXTRA_RRECOMMENDS",
        "DISTRO_FEATURES",
        "DISTRO_FEATURES_BACKFILL",
        "DISTRO_FEATURES_BACKFILL_CONSIDERED",
        "DISTRO_FEATURES_DEFAULT",
        "DISTRO_FEATURES_OPTED_OUT",
    ])
    @pytest.mark.parametrize('filename', [
        'conf/layer.conf',
    ])
    def test_bad_layer(self, id_, var, filename, occurrence):
        input_ = {
            filename: self.__generate_sample_code(var),
        }
        self.check_for_id(self._create_args(
            input_, extraopts=['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.outofcontext'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        "MACHINE",
        "MACHINEOVERRIDES",
        "MACHINE_ESSENTIAL_EXTRA_RDEPENDS",
        "MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS",
        "MACHINE_EXTRA_RRECOMMENDS",
        "MACHINE_FEATURES",
        "MACHINE_FEATURES_BACKFILL",
        "MACHINE_FEATURES_OPTED_OUT",
    ])
    @pytest.mark.parametrize('filename', [
        'conf/machine/test.conf',
    ])
    def test_good_machine(self, id_, var, filename, occurrence):
        input_ = {
            filename: self.__generate_sample_code(var),
        }
        self.check_for_id(self._create_args(
            input_, extraopts=['--mode=all']), id_, occurrence)

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
        "DISTRO_FEATURES_OPTED_OUT",
    ])
    @pytest.mark.parametrize('filename', [
        'conf/distro/test.conf',
    ])
    def test_good_distro(self, id_, var, filename, occurrence):
        input_ = {
            filename: self.__generate_sample_code(var),
        }
        self.check_for_id(self._create_args(
            input_, extraopts=['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.outofcontext'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        "BBFILES",
        "BBFILES_DYNAMIC",
        "BBFILE_COLLECTIONS",
        "BBPATH",
        "HOSTTOOLS_NONFATAL",
        "LICENSE_PATH",
    ])
    @pytest.mark.parametrize('filename', [
        'conf/layer.conf',
    ])
    def test_good_layer(self, id_, var, filename, occurrence):
        input_ = {
            filename: self.__generate_sample_code(var),
        }
        self.check_for_id(self._create_args(
            input_, extraopts=['--mode=all']), id_, occurrence)
