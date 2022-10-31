import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsSectionLowerCase(TestBaseClass):

    def __generate_sample_code(self, op):
        return '''
            VAR{op}"1"
            '''.format(op=op)

    @pytest.mark.parametrize('id_', ['oelint.vars.spacesassignment'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('op',
                             [
                                 ' :=',
                                 ' ??=',
                                 ' ?=',
                                 ' .=',
                                 ' +=',
                                 ' =.',
                                 ' =',
                                 ' =+',
                                 ':= ',
                                 ':=',
                                 '??= ',
                                 '??=',
                                 '?= ',
                                 '?=',
                                 '.= ',
                                 '.=',
                                 '+= ',
                                 '+=',
                                 '= ',
                                 '=. ',
                                 '=.',
                                 '=',
                                 '=+ ',
                                 '=+',
                             ],
                             )
    def test_bad(self, op, id_, occurrence):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(op),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.spacesassignment'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('op',
                             [
                                 ' = ',
                                 ' =. ',
                                 ' .= ',
                                 ' += ',
                                 ' =+ ',
                                 ' ?= ',
                                 ' ??= ',
                                 ' := ',
                             ],
                             )
    def test_good(self, op, id_, occurrence):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(op),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)
