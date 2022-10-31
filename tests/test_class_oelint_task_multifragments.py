import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintTaskMultiAppends(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.task.multifragments'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         a
                                     }
                                     do_install_append() {
                                         b
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_configure_append() {
                                         a
                                     }
                                     do_configure_append() {
                                         b
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_custom_append() {
                                         a
                                     }
                                     do_custom_append() {
                                         b
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.multifragments'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         a
                                     }
                                     do_install_append_class-native() {
                                         a
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         a
                                     }
                                     do_install_append_class-nativesdk() {
                                         a
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         a
                                     }
                                     do_install_append_class-cross() {
                                         a
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         a
                                     }
                                     do_install_append_class-target() {
                                         a
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         a
                                     }
                                     do_install_prepend() {
                                         a
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         a
                                     }
                                     do_somethingelse_append() {
                                         a
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
