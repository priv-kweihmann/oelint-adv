import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsOverrideAppend(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.overrideappend'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:class-target:append = " a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:class-target:prepend = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:qemux86-64:prepend = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A:class-target += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'ALTERNATIVE:${PN}:foo =+ "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'ALTERNATIVE:${PN}-test:foo =+ "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A:class-target =. "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS:class-native:append = "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SUMMARY:${PN}:class-native += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DESCRIPTION:${PN}:class-native .= "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'LICENSE:${PN}:class-native =. "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SECTION:${PN}:class-native += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SUMMARY:class-native .= "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DESCRIPTION:class-native =+ "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'LICENSE:class-native += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SECTION:class-native += "a"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.overrideappend'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'FILES:${PN}-ptest:append:class-target = " a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'ALTERNATIVE:${PN}:append = " xxd"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     B:class-target = ""
                                     B:class-target:append = " a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     B:class-target:qemux86-64 = ""
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     FILES:${PN} = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'ALTERNATIVE:${PN} += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:class-target = ""
                                     A:class-target =+ "a"
                                     '''
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SUMMARY:${PN} += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SECTION:${PN} += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DESCRIPTION:${PN} += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'LICENSE:${PN} += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SUMMARY += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SECTION += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DESCRIPTION += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'LICENSE += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     PACKAGES_DYNAMIC = "^${PN}-lib.*"
                                     LICENSE:${PN}-libfoo += "a"
                                     '''
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.overrideappend'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:class-target:append = " a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:class-target:prepend = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A:qemux86-64:prepend = "a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A:class-target += " a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A:class-target .= "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'ALTERNATIVE:${PN}:foo =+ "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'ALTERNATIVE:${PN}-test:foo =+ "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A:class-target =. "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SUMMARY:${PN}:class-native += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DESCRIPTION:${PN}:class-native .= "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'LICENSE:${PN}:class-native =. "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SECTION:${PN}:class-native += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SUMMARY:class-native .= "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DESCRIPTION:class-native =+ "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'LICENSE:class-native += "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SECTION:class-native += "a"',
                                 },
                             ],
                             )
    def test_fix(self, input_, id_, occurrence):
        self.fix_and_check(self._create_args_fix(input_), id_)
