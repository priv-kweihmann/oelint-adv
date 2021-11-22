import pytest

from .base import TestBaseClass


class TestClassOelintTaskNoMkdir(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.task.nomkdir'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input',
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
                             ],
                             )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.task.nomkdir'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input',
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
                             ],
                             )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
