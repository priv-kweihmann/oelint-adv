import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintTaskDocstrings(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.task.docstrings'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo() {
                                         :
                                     }
                                     addtask do_foo
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.docstrings'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo() {
                                         :
                                     }
                                     addtask do_foo
                                     do_foo[doc] = "Fooo!!!!"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo:append() {
                                         :
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo[doc] = "Fooo!!!!"
                                     do_foo() {
                                         :
                                     }
                                     addtask do_foo
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     python () {
                                         print("Hello world")
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     python __anonymous () {
                                         print("Hello world")
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
