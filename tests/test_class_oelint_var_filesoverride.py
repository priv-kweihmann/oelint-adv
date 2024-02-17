import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarFilesOverride(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.var.filesoverride'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES:${PN} = " foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES:${PN} := "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES:${PN}-dev = "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES:${PN}-dev := "foo"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.filesoverride'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES_${PN} = " foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES_${PN} := "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES_${PN}-dev = "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES_${PN}-dev := "foo"',
                                 },
                             ],
                             )
    def test_bad_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.filesoverride'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES:SOLIBSDEV = "abc"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES:${PN}:append = " foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES:${PN}:prepend = "foo "',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES:${PN} += "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES:${PN} =+ "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES:${PN} .= " foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES:${PN} =. "foo "',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES:${PN}-dev += "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES:${PN}-dev =+ "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES:${PN}-dev .= " foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES:${PN}-dev =. "foo "',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.filesoverride'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES_SOLIBSDEV = "abc"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES_${PN}_append = " foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES_${PN}_prepend = "foo "',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES_${PN} += "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES_${PN} =+ "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES_${PN} .= " foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES_${PN} =. "foo "',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES_${PN}-dev += "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES_${PN}-dev =+ "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES_${PN}-dev .= " foo"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'FILES_${PN}-dev =. "foo "',
                                 },
                             ],
                             )
    def test_good_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)
