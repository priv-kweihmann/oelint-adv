import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarSuggestedVar(TestBaseClass):

    def __generate_sample_code(self, var, extra):
        return '''
            {extra}
            {var} = "foo"
            '''.format(var=var, extra=extra)

    @pytest.mark.parametrize('id_', ['oelint.var.suggestedvar'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'BUGTRACKER',
        'CVE_PRODUCT',
        'SECTION',
    ])
    def test_bad(self, id_, occurrence, var):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code('A', ''),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.suggestedvar.CVE_PRODUCT'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint-adv_test.bb':
                                     'VAR = "a"',
                                 },
                             ],
                             )
    def test_suppress(self, id_, occurrence, input_):
        _x = self._create_args(input_, extraopts=['--suppress', id_])
        self.check_for_id(_x, id_, occurrence)
        self.check_for_id(_x, 'oelint.var.suggestedvar.BUGTRACKER', 1)

    @pytest.mark.parametrize('id_', [
        'oelint.var.suggestedvar.BUGTRACKER',
        'oelint.var.suggestedvar.BBCLASSEXTEND',
        'oelint.var.suggestedvar.CVE_PRODUCT',
        'oelint.var.suggestedvar.SECTION',
    ])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     BUGTRACKER = "1"
                                     BBCLASSEXTEND = "1"
                                     CVE_PRODUCT = "1"
                                     SECTION = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
