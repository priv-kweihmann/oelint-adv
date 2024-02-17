import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsInsaneSkip(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.insaneskip'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'INSANE_SKIP:${PN} = "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'INSANE_SKIP:bla = "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'INSANE_SKIP:bla:class-native = "a"',
                                 },

                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.insaneskip'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'INSANE_SKIP_${PN} = "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'INSANE_SKIP_bla = "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'INSANE_SKIP_bla_class-native = "a"',
                                 },
                             ],
                             )
    def test_bad_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.insaneskip'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'VAR += "ffjjj"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
