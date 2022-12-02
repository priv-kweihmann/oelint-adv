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
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

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
                                     DEPENDS += "foo"
                                     DEPENDS_class-native += "foo"
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
                                     DEPENDS += "foo"
                                     DEPENDS_remove = "foo"
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
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
