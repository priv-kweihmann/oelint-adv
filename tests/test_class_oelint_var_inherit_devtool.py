import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarInheritDevtool(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.var.inheritdevtool.native'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit native',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit def ${@oe.utils.vartrue("X", "native", "", d)}
                                     ''',
                                 },
                             ],
                             )
    def test_bad_inherit_native(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=scarthgap']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.inheritdevtool.nativesdk'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit nativesdk',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit def ${@oe.utils.vartrue("X", "nativesdk", "", d)}
                                     ''',
                                 },
                             ],
                             )
    def test_bad_inherit_nativesdk(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=scarthgap']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.inheritdevtool.native'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer native
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer ${@oe.utils.ifelse(1 == 1, 'native', C}
                                     ''',
                                 },
                             ],
                             )
    def test_good_inherit_native(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=scarthgap']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.inheritdevtool.nativesdk'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer nativesdk
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer ${@oe.utils.ifelse(1 == 1, 'nativesdk', C}
                                     ''',
                                 },
                             ],
                             )
    def test_good_inherit_nativesdk(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=scarthgap']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.inheritdevtool.cross'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer cross
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer ${@oe.utils.ifelse(1 == 1, 'cross', C}
                                     ''',
                                 },
                             ],
                             )
    def test_good_inherit_cross(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=scarthgap']), id_, occurrence)
