import pytest  # noqa: I900
from oelint_parser.constants import CONSTANTS

from .base import TestBaseClass


class TestClassOelintVarsOutOfContextConf(TestBaseClass):

    def __generate_sample_code(self, var, extra=''):
        return '''
            {extra}
            {var} = "foo"
            '''.format(var=var, extra=extra)

    @pytest.mark.parametrize('id_', ['oelint.vars.outofcontext'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        "EXTRA_IMAGE_FEATURES",
        "IMAGE_FEATURES",
    ])
    @pytest.mark.parametrize('extra', [
        '',
        'inherit something',
    ])
    def test_bad(self, id_, var, extra, occurrence):
        input_ = {
            'test.bb': self.__generate_sample_code(var, extra),
        }
        self.check_for_id(self._create_args(input_, extraopts=['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.outofcontext'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        "EXTRA_IMAGE_FEATURES",
        "IMAGE_FEATURES",
    ])
    @pytest.mark.parametrize('extra', [
        *[f'inherit {x}' for x in CONSTANTS.ImagesClasses],
    ])
    def test_good(self, id_, var, extra, occurrence):
        input_ = {
            'test.bb': self.__generate_sample_code(var, extra),
        }
        self.check_for_id(self._create_args(input_, extraopts=['--mode=all']), id_, occurrence)
