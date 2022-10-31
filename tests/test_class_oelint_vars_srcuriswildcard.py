import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarSRCURIWildcard(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.var.srcuriwildcard'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "file://*"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SRC_URI += "git://foo.org;name=${PV} \\
                                         file://somedir/*"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.srcuriwildcard'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI = "git://foo.org;name=${PV}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "${@["", "file://init.cfg"][(d.getVar(\'VIRTUAL-RUNTIME_init_manager\') == \'busybox\')]}"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
