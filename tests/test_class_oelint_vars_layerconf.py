import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsLayerConf(TestBaseClass):

    def __generate_sample_code(self, var, operation):
        return '''
            {var} {operation} "foo"
            '''.format(var=var, operation=operation)

    @pytest.mark.parametrize('id_', ['oelint.vars.layerconf'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'BBFILES',
        'BBFILES_DYNAMIC',
        'BBFILE_COLLECTIONS',
        'BBFILE_PATTERN_foo',
        'BBFILE_PRIORITY_foo',
        'BBPATH',
        'HOSTTOOLS_NONFATAL',
        'LAYERDEPENDS_foo',
        'LAYERRECOMMENDS_foo',
        'LAYERSERIES_COMPAT_foo',
        'LAYERVERSION_foo',
        'LICENSE_PATH',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', '.=', '=.', '+=', '=+', ' =+'])
    def test_good(self, id_, var, operation, occurrence):
        input_ = {
            'conf/layer.conf': self.__generate_sample_code(var, operation),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.layerconf'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'BBFILES',
        'BBFILES_DYNAMIC',
        'BBFILE_COLLECTIONS',
        'BBFILE_PATTERN_foo',
        'BBFILE_PRIORITY_foo',
        'BBPATH',
        'HOSTTOOLS_NONFATAL',
        'LAYERDEPENDS_foo',
        'LAYERRECOMMENDS_foo',
        'LAYERSERIES_COMPAT_foo',
        'LAYERVERSION_foo',
        'LICENSE_PATH',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', '.=', '=.', '+=', '=+', ' =+'])
    def test_good_non_layer(self, id_, var, operation, occurrence):
        input_ = {
            'oelint-test_1.0.bb': self.__generate_sample_code(var, operation),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.layerconf'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'SOME_OTHER_VAR',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', '.=', '=.', '+=', '=+', ' =+'])
    def test_bad(self, id_, var, operation, occurrence):
        input_ = {
            'conf/layer.conf': self.__generate_sample_code(var, operation),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)
