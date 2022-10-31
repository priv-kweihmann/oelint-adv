import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintTaskNoPythonPrefix(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.task.nopythonprefix'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     python do_foo() {
                                         mkdir -p ${TMP}sjdsdasjdha
                                         ./configure
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.nopythonprefix'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo() {
                                         mkdir -p ${TMP}sjdsdasjdha
                                         ./configure
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     python do_bar() {
                                         import os
                                         print("fooooooo!!!!")
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
