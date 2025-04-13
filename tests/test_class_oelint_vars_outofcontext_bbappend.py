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
        "FILESEXTRAPATHS",
    ])
    @pytest.mark.parametrize('filename', [
        'test_.bb',
        'classes/test.bbclass',
        'conf/machine/test.conf',
        'conf/layer.conf',
        'conf/distro/test.conf',
    ])
    def test_bad(self, id_, var, filename, occurrence):
        input_ = {
            filename: self.__generate_sample_code(var),
        }
        self.check_for_id(self._create_args(input_, extraopts=['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.outofcontext'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        "FILESEXTRAPATHS",
    ])
    @pytest.mark.parametrize('filename', [
        'test_%.bbappend',
    ])
    def test_good(self, id_, var, filename, occurrence):
        input_ = {
            filename: self.__generate_sample_code(var),
        }
        self.check_for_id(self._create_args(input_, extraopts=['--mode=all']), id_, occurrence)
