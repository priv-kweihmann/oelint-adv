import pytest

from .base import TestBaseClass


class TestClassOelintVarsClass(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.dependsclass'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input',
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
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.dependsappend'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input',
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
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
