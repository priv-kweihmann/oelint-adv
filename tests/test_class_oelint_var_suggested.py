import pytest
from base import TestBaseClass


class TestClassOelintVarSuggestedVar(TestBaseClass):

    def __generate_sample_code(self, var, extra):
        return '''
            {extra}
            {var} = "foo"
            '''.format(var=var, extra=extra)

    @pytest.mark.parametrize('id', ['oelint.var.suggestedvar'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        "AUTHOR",
        "BUGTRACKER",
        "BBCLASSEXTEND",
        "CVE_PRODUCT",
        "SECTION",
    ])
    def test_bad(self, id, occurrence, var):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code('A', '')
        }
        id += '.{}'.format(var)
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.var.suggestedvar.CVE_PRODUCT'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint-adv_test.bb':
            '''
            VAR = "a"
            '''
            },
        ]
    )
    def test_suppress(self, id, occurrence, input):
        _x = self._create_args(input, extraopts=["--suppress", id])
        self.check_for_id(_x, id, occurrence)
        self.check_for_id(_x, 'oelint.var.suggestedvar.BUGTRACKER', 1)

    @pytest.mark.parametrize('id', [
        'oelint.var.suggestedvar.AUTHOR',
        'oelint.var.suggestedvar.BUGTRACKER',
        'oelint.var.suggestedvar.BBCLASSEXTEND',
        'oelint.var.suggestedvar.CVE_PRODUCT',
        'oelint.var.suggestedvar.SECTION',
        ])
    @pytest.mark.parametrize('occurrence', [0])
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
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)


 
