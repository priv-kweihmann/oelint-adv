import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsFilextrapaths(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.fileextrapaths'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'FILESEXTRAPATHS:prepend := "${THISDIR}/file"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILESEXTRAPATHS:append := "${THISDIR}/file"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILESEXTRAPATHS += "${THISDIR}/file"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.fileextrapaths'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'FILESEXTRAPATHS_prepend := "${THISDIR}/file"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILESEXTRAPATHS_append := "${THISDIR}/file"',
                                 },
                             ],
                             )
    def test_bad_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.fileextrapaths'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILESEXTRAPATHS:prepend := "${THISDIR}/file"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILESEXTRAPATHS:append := "${THISDIR}/file"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.fileextrapaths'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILESEXTRAPATHS_prepend := "${THISDIR}/file"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILESEXTRAPATHS_append := "${THISDIR}/file"',
                                 },
                             ],
                             )
    def test_good_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)
