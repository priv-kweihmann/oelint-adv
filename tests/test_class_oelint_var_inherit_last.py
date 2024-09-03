import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarInheritLast(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.var.inheritlast.native'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit native
                                     inherit foo
                                     ''',
                                 },
                             ],
                             )
    def test_bad_inherit_native(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.inheritlast.nativesdk'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit nativesdk
                                     inherit foo
                                     ''',
                                 },
                             ],
                             )
    def test_bad_inherit_nativesdk(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.inheritlast.cross'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit cross
                                     inherit foo
                                     ''',
                                 },
                             ],
                             )
    def test_bad_inherit_cross(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.inheritlast',
                                     'oelint.var.inheritlast.native',
                                     'oelint.var.inheritlast.nativesdk',
                                     'oelint.var.inheritlast.cross'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit abc native
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit abc nativesdk
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit abc cross
                                     ''',
                                 },
                             ],
                             )
    def test_good_inherit(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
