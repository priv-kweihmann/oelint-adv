import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarInherit(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.var.inherit.inherit_defer'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit ${A}',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit def ${C}
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit def ${@oe.utils.ifelse(1 == 1, 'a', C}
                                     ''',
                                 },
                             ],
                             )
    def test_bad_inherit(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=scarthgap']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.inherit.inherit'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit_defer A',
                                 },
                             ],
                             )
    def test_bad_inherit_defer(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=scarthgap']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.inherit.inherit'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit abc def
                                     ''',
                                 },
                             ],
                             )
    def test_good_inherit(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=scarthgap']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.inherit.inherit_defer'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer ${A}
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer native
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer nativesdk
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer cross
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer abc ${A}
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit_defer ${@oe.utils.ifelse(1 == 1, 'a', C}
                                     ''',
                                 },
                             ],
                             )
    def test_good_inherit_defer(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=scarthgap']), id_, occurrence)
