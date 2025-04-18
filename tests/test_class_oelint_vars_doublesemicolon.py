import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsAutorev(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.doublesemicolon'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        "LIC_FILES_CHKSUM",
        "SRC_URI",
    ])
    def test_bad(self, var, id_, occurrence):
        input_ = {
            'test.bb': f'{var} = "foo;;bar;;;;baz;;a=1;b=2"\n',
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.doublesemicolon'])
    @pytest.mark.parametrize('var', [
        "LIC_FILES_CHKSUM",
        "SRC_URI",
    ])
    def test_fix(self, var, id_):
        input_ = {
            'test.bb': f'{var} = "foo;;bar;;;;baz;;a=1;b=2"\n',
        }
        self.fix_and_check(self._create_args_fix(input_), id_)

    @pytest.mark.parametrize('id_', ['oelint.vars.doublesemicolon'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        "LIC_FILES_CHKSUM",
        "SRC_URI",
    ])
    def test_good(self, var, id_, occurrence):
        input_ = {
            'test.bb': f'{var} = "foo;bar;baz;a=1;b=2"\n',
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)
