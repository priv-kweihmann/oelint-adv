import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsSectionLowerCase(TestBaseClass):

    def __generate_sample_code(self, op):
        return '''
            VAR{op}"1"
            '''.format(op=op)

    @pytest.mark.parametrize('id', ['oelint.vars.spacesassignment'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('op', 
        [
            " :=",
            " ??=",
            " ?=",
            " .=",
            " +=",
            " =.",
            " =",
            " =+",
            ":= ",
            ":=",
            "??= ",
            "??=",
            "?= ",
            "?=",
            ".= ",
            ".=",
            "+= ",
            "+=",
            "= ",
            "=. ",
            "=.",
            "=",
            "=+ ",
            "=+",
        ],
    )
    def test_bad(self, op, id, occurrence):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(op)
        }
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.spacesassignment'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('op', 
        [
            " = ",
            " =. ",
            " .= ",
            " += ",
            " =+ ",
            " ?= ",
            " ??= ",
            " := ",
        ],
    )
    def test_good(self, op, id, occurrence):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(op)
        }
        self.check_for_id(self._create_args(input), id, occurrence)
