import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintAppendProtVars(TestBaseClass):

    def __generate_sample_code(self, var, operation):
        return '{var} {operation} "foo"'.format(var=var, operation=operation)

    @pytest.mark.parametrize('id_', ['oelint.append.protvars'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'PV',
        'PR',
        'SRCREV',
        'LICENSE',
        'LIC_FILES_CHKSUM',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', ' :='])
    def test_bad(self, id_, occurrence, var, operation):
        input_ = {
            'oelint_adv_test.bbappend': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.append.protvars'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'PV',
        'PR',
        'SRCREV',
        'LICENSE',
        'LIC_FILES_CHKSUM',
    ])
    @pytest.mark.parametrize('operation', ['?=', '??=', ' ??='])
    def test_good_weak(self, id_, occurrence, var, operation):
        input_ = {
            'oelint_adv_test.bbappend': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.append.protvars'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'PV',
        'PR',
        'SRCREV',
        'LICENSE',
        'LIC_FILES_CHKSUM',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', ' :='])
    def test_good_bb(self, id_, occurrence, var, operation):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.append.protvars'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'PV[vardeps]',
        'PV[vardepsexclude]',
        'PV[vardepvalue]',
        'PV[vardepvalueexclude]',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', ' :='])
    def test_good_flags(self, id_, occurrence, var, operation):
        input_ = {
            'oelint_adv_test.bbappend': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)
