import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsInAppClassOverride(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.inappclassoverride'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'A:class-native = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A:class-nativesdk = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:class-native = "1"
                                     BBCLASSEXTEND = "nativesdk"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:class-nativesdk = "1"
                                     BBCLASSEXTEND = "native"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_a:append:class-native() {
                                        :
                                     }
                                     BBCLASSEXTEND = "nativesdk"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_a:append:class-nativesdk() {
                                        :
                                     }
                                     BBCLASSEXTEND = "native"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_a:append:class-native() {
                                        :
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_a:append:class-nativesdk() {
                                        :
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.inappclassoverride'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:class-native = "1"
                                     inherit native
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:class-nativesdk = "1"
                                     inherit nativesdk
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:class-native = "1"
                                     BBCLASSEXTEND = "native"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:class-nativesdk = "1"
                                     BBCLASSEXTEND = "nativesdk"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bbclass':
                                     'A:class-native = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bbclass':
                                     'A:class-nativesdk = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'A:class-native = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bbappend':
                                     'A:class-nativesdk = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_a:append:class-native() {
                                        :
                                     }
                                     BBCLASSEXTEND = "native"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_a:append:class-nativesdk() {
                                        :
                                     }
                                     BBCLASSEXTEND = "nativesdk"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_a:append:class-native() {
                                        :
                                     }
                                     inherit native
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_a:append:class-nativesdk() {
                                        :
                                     }
                                     inherit nativesdk
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
