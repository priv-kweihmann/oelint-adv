import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsPythonRdepends(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.pythonrdepends'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} = "${PYTHON_PN}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} = "python"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} = "python3"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.pythonrdepends'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} = "${PYTHON_PN}-core"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} = "python-core"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} = "python3-core"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} = "python3-somethingelse"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
