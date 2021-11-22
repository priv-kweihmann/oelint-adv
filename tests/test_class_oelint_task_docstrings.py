import pytest

from .base import TestBaseClass


class TestClassOelintTaskDocstrings(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.task.docstrings'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input',
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
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.task.docstrings'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input',
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
                                     do_foo[doc] = "Fooo!!!!"
                                     do_foo() {
                                         :
                                     }
                                     addtask do_foo
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
