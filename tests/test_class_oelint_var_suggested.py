import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarSuggestedVar(TestBaseClass):

    def __generate_sample_code(self, var, extra):
        return '''
            {extra}
            {var} = "foo"
            '''.format(var=var, extra=extra)

    @pytest.mark.parametrize('id', ['oelint.var.suggestedvar'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('var', [
        "AUTHOR",
        "BUGTRACKER",
        "BBCLASSEXTEND",
        "CVE_PRODUCT",
        "SECTION",
    ])
    def test_bad(self, id, occurance, var):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code('A', '')
        }
        id += '.{}'.format(var)
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', [
        'oelint.var.suggestedvar.AUTHOR',
        'oelint.var.suggestedvar.BUGTRACKER',
        'oelint.var.suggestedvar.BBCLASSEXTEND',
        'oelint.var.suggestedvar.CVE_PRODUCT',
        'oelint.var.suggestedvar.SECTION',
        ])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            BUGTRACKER = "1"
            BBCLASSEXTEND = "1"
            CVE_PRODUCT = "1"
            AUTHOR = "foo"
            SECTION = "foo"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)


 
