import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsListAppend(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.listappend'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'PACKAGES =. "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES:${PN}-tracepath:append = "${base_bindir}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} .= "bar"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS:prepend = "xyz"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI .= "file://abc"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.listappend'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'PACKAGES =. "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES_${PN}-tracepath_append = "${base_bindir}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS_${PN} .= "bar"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS_prepend = "xyz"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI .= "file://abc"',
                                 },
                             ],
                             )
    def test_bad_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.listappend'])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'PACKAGES =. "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES:${PN}-tracepath:append = "${base_bindir}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} .= "bar"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS:prepend = "xyz"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI .= "file://abc"',
                                 },
                             ],
                             )
    def test_fix(self, input_, id_):
        self.fix_and_check(self._create_args_fix(input_), id_)

    @pytest.mark.parametrize('id_', ['oelint.vars.listappend'])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'PACKAGES =. "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES_${PN}-tracepath_append = "${base_bindir}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS_${PN} .= "bar"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS_prepend = "xyz"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI .= "file://abc"',
                                 },
                             ],
                             )
    def test_fix_old(self, input_, id_):
        self.fix_and_check(self._create_args_fix(input_, ['--release=dunfell']), id_)

    @pytest.mark.parametrize('id_', ['oelint.vars.listappend'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'PACKAGES =. "foo "',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES:${PN}-tracepath:append = " ${base_bindir}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} .= " bar"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS:prepend = "xyz "',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI .= " file://abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILESPATH:prepend := "${THISDIR}/file:"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILESEXTRAPATHS:prepend := "${THISDIR}/file:"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.listappend'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'PACKAGES =. "foo "',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES_${PN}-tracepath_append = " ${base_bindir}"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS_${PN} .= " bar"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS_prepend = "xyz "',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI .= " file://abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILESPATH_prepend := "${THISDIR}/file:"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILESEXTRAPATHS_prepend := "${THISDIR}/file:"',
                                 },
                             ],
                             )
    def test_good_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)
