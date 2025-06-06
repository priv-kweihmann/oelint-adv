import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintTaskNoMkdir(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.task.nomkdir'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install() {
                                         mkdir -p ${TMP}sjdsdasjdha
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                        mkdir -p ${TMP}sjdsdasjdha
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                        test 123 & mkdir -p ${TMP}sjdsdasjdha
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.nomkdir'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install() {
                                         install -d ${TMP}sjdsdasjdha
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_compile() {
                                         mkdir -p ${TMP}sjdsdasjdha
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     # nooelint: oelint.task.nomkdir
                                     do_install() {
                                        some operation
                                        mkdir -p ${TMP}sjdsdasjdha
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
