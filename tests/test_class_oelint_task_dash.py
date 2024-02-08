import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintTaskDash(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.task.dash'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do-install() {
                                        :
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     addtask do-install
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     deltask do-install
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do-install():
                                         pass
                                     # a comment
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.dash'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install() {
                                         :
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     addtask do_install
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     deltask do_install
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_install():
                                          pass
                                     # a comment
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
