import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintTaskCustomOrder(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.task.customorder'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     addtask do_compile after do_configure
                                     addtask do_configure after do_compile
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo() {
                                         :
                                     }
                                     addtask do_compile after do_configure
                                     addtask do_foo before do_configure after do_compile
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.customorder'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     addtask do_compile after do_foo
                                     addtask do_configure after do_compile
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
