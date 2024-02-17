import pytest  # noqa: I900
from .base import TestBaseClass


class TestClassOelintJetmDependsSingleLine(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.jetm.vars.dependssingleline'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS += "abc def"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "ghi \\
                                         jkl"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} += "abc def"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} += "ghi \\
                                         jkl"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, extraopts=[
                          '--addrules=jetm']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.jetm.vars.dependssingleline'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS_${PN} += "abc def"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS_${PN} += "ghi \\
                                         jkl"
                                     ''',
                                 },
                             ],
                             )
    def test_bad_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, extraopts=[
                          '--addrules=jetm', '--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.jetm.vars.dependssingleline'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "abc"
                                     DEPENDS += "def"
                                     DEPENDS += "ghi"
                                     DEPENDS += "jkl"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} += "abc"
                                     RDEPENDS:${PN} += "def"
                                     RDEPENDS:${PN} += "ghi"
                                     RDEPENDS:${PN} += "jkl"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "abc (>= 1.2.3)"
                                     DEPENDS += "def (<= 4.5.6)"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, extraopts=[
                          '--addrules=jetm']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.jetm.vars.dependssingleline'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS_${PN} += "abc"
                                     RDEPENDS_${PN} += "def"
                                     RDEPENDS_${PN} += "ghi"
                                     RDEPENDS_${PN} += "jkl"
                                     ''',
                                 },
                             ],
                             )
    def test_good_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, extraopts=[
                          '--addrules=jetm', '--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.jetm.vars.dependssingleline'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS += "abc def"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "ghi \\
                                         jkl"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} += "abc def"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} += "ghi \\
                                         jkl"
                                     ''',
                                 },
                             ],
                             )
    def test_good_module_off(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.jetm.vars.dependssingleline'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS += "abc def"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "ghi \\
                                         jkl"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS_${PN} += "abc def"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS_${PN} += "ghi \\
                                         jkl"
                                     ''',
                                 },
                             ],
                             )
    def test_good_module_off_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)
