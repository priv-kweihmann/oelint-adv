import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarFilesOverride(TestBaseClass):

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
    def test_bad(self, input_, id_, occurrence):
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
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
