import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintTaskNoCopy(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.task.nocopy'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         cp A B
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         cp * B
                                     }
                                     ''',
                                 },
                                 {
                                    'oelint_adv_test.bb':
                                    '''
                                    do_install_append() {
                                        otherop --no-preserve=ownership && cp * B
                                    }
                                    ''',
                                },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.nocopy'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         install A B
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     # nooelint: oelint.task.nocopy
                                     do_install_append() {
                                         cp A B
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         cp -r A
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         cp -R A
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         cp --no-preserve=ownership A
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         cp -R --no-preserve=ownership A
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                         '''
                                         do_install_append() {
                                             install file-name-which-contains-tcp B
                                         }
                                         ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
