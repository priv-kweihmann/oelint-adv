import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsDuplicate(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.duplicate'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS = "foo"
                                     DEPENDS += "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} = "foo"
                                     RDEPENDS:${PN}:prepend = " foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN}-dev = "foo"
                                     RDEPENDS:${PN}-dev:prepend = " foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN}:class-target = "foo"
                                     RDEPENDS:${PN}:append:class-target = "foo "
                                     ''',
                                 },
                                 {
                                     'oelint-adv-test_1.0.bb': '',
                                     'dynamic-layers/a/oelint-adv-test_1.0.bbappend':
                                     '''
                                     DEPENDS += "a"
                                     ''',
                                     'dynamic-layers/a/oelint-adv-test_%.bbappend':
                                     '''
                                     DEPENDS += "a"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.duplicate'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS = "foo"
                                     DEPENDS_append = " foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS = "foo"
                                     DEPENDS_prepend = " foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS_${PN} = "foo"
                                     RDEPENDS_${PN}_prepend = " foo"
                                     ''',
                                 },
                             ],
                             )
    def test_bad_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.duplicate'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "foo"
                                     DEPENDS = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "${@inline.block}"
                                     DEPENDS += "${@inline.block}"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "a (>= 1.2.3)"
                                     DEPENDS += "b (>= 1.2.3)"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN}:class-target = "foo"
                                     RDEPENDS:${PN} = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb': '',
                                     'dynamic-layers/a/oelint_adv_test.bbappend':
                                     '''
                                     DEPENDS += "a"
                                     ''',
                                     'dynamic-layers/b/oelint_adv_test.bbappend':
                                     '''
                                     DEPENDS += "a"
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.duplicate'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "foo"
                                     DEPENDS_class-native += "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "foo"
                                     DEPENDS_remove = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_good_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)
