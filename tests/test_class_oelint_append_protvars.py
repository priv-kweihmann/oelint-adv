import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintAppendProtVars(TestBaseClass):

    def __generate_sample_code(self, var, operation):
        return '''
            {var} {operation} "foo"
            '''.format(var=var, operation=operation)

    @pytest.mark.parametrize('id', ['oelint.append.protvars'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('var', [
            "PV",
            "PR",
            "SRCREV",
            "LICENSE",
            "LIC_FILES_CHKSUM"
    ])
    @pytest.mark.parametrize('operation', ['=', ':='])
    def test_bad(self, id, occurance, var, operation):
        input = {
            'oelint_adv_test.bbappend': self.__generate_sample_code(var, operation)
        }
        id += '.{}'.format(var)
        self.check_for_id(self._create_args(input), id, occurance)


    @pytest.mark.parametrize('id', ['oelint.append.protvars'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('var', [
            "PV",
            "PR",
            "SRCREV",
            "LICENSE",
            "LIC_FILES_CHKSUM"
    ])
    @pytest.mark.parametrize('operation', ['?=', '??='])
    def test_good_weak(self, id, occurance, var, operation):
        input = {
            'oelint_adv_test.bbappend': self.__generate_sample_code(var, operation)
        }
        id += '.{}'.format(var)
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.append.protvars'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('var', [
            "PV",
            "PR",
            "SRCREV",
            "LICENSE",
            "LIC_FILES_CHKSUM"
    ])
    @pytest.mark.parametrize('operation', ['=', ':='])
    def test_good_bb(self, id, occurance, var, operation):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(var, operation)
        }
        id += '.{}'.format(var)
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.append.protvars'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('var', [
            "PV[vardeps]",
            "PV[vardepsexclude]",
            "PV[vardepvalue]",
            "PV[vardepvalueexclude]",
    ])
    @pytest.mark.parametrize('operation', ['=', ':='])
    def test_good_flags(self, id, occurance, var, operation):
        input = {
            'oelint_adv_test.bbappend': self.__generate_sample_code(var, operation)
        }
        id += '.{}'.format(var)
        self.check_for_id(self._create_args(input), id, occurance)