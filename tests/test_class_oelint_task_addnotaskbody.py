import pytest  # noqa: I900

from .base import TestBaseClass

# flake8: noqa W293 - we want to explicitly test lines with just whitespaces here

class TestClassOelintTaskAddNoBody(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.task.addnotaskbody'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo() {
                                     
                                     }
                                     addtask do_foo
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     addtask do_notexists
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo() {
                                     
                                     }
                                     addtask foo
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.addnotaskbody'])
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
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo() {
                                         :
                                     }
                                     addtask foo
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     addtask build
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     addtask configure
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     addtask compile
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     addtask install
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
