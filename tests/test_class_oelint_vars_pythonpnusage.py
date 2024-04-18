import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsPythonPnUsage(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.pythonpnusage'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'A = "${PYTHON_PN}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A = "${PYTHON_PN}/${PYTHON_PN}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A_${PYTHON_PN} = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_something() {
                                        echo ${PYTHON_PN} > test.txt
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.getVar("PYTHON_PN")
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.getVar(\'PYTHON_PN\')
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.expandVar("${PYTHON_PN}/A")
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=scarthgap']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.pythonpnusage'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'A = "${PYTHON_PN}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A = "${PYTHON_PN}/${PYTHON_PN}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A_${PYTHON_PN} = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_something() {
                                        echo ${PYTHON_PN} > test.txt
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.getVar("PYTHON_PN")
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.getVar(\'PYTHON_PN\')
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.expandVar("${PYTHON_PN}/A")
                                     ''',
                                 },
                             ],
                             )
    def test_bad_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=nanbield']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.pythonpnusage'])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'A = "${PYTHON_PN}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A = "${PYTHON_PN}/${PYTHON_PN}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A_${PYTHON_PN} = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_something() {
                                        echo ${PYTHON_PN} > test.txt
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.getVar("PYTHON_PN")
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.getVar(\'PYTHON_PN\')
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.expandVar("${PYTHON_PN}/A")
                                     ''',
                                 },
                             ],
                             )
    def test_fix(self, input_, id_):
        self.fix_and_check(self._create_args_fix(input_, ['--release=scarthgap']), id_)

    @pytest.mark.parametrize('id_', ['oelint.vars.pythonpnusage'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'S = "${WORDKIR}/${BP}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRCREV_PYTHON_PN = "01234567890abcdef"',
                                 },
                                 {
                                     'classes/test.bbclass':
                                     'A = "${PYTHON_PN}"',
                                     'oelint_adv_test.bb':
                                     'inherit test',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A = "python3"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A = "python3/python3"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A_python3 = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_something() {
                                        echo python3 > test.txt
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.getVar("somethingelse")
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.getVar(\'somethingelse\')
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     def do_something():
                                        d.expandVar("python3/A")
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=scarthgap']), id_, occurrence)
