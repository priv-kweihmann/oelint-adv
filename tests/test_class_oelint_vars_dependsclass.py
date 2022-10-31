import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsClass(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.dependsclass'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit native
                                     DEPENDS = "bar"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit nativesdk
                                     DEPENDS = "bar"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit native
                                     DEPENDS = "nativesdk-bar"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit native
                                     DEPENDS = "nativesdk-bar foo-native"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.dependsappend'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit native
                                     DEPENDS += "foo-native"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit nativesdk
                                     DEPENDS += "nativesdk-foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS = "foo-native"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS = "nativesdk-foo"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
