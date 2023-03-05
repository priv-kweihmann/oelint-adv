import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsDependsOrdered(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.dependsordered'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "zzz \\
                                     xyz"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "foo"
                                     DEPENDS += "bar"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} += "zzz \\
                                                 xyz"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} += "foo"
                                     RDEPENDS:${PN} += "bar"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.dependsordered'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "bar"
                                     DEPENDS += "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "xyz \\
                                                 zzz"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} += "bar"
                                     RDEPENDS:${PN} += "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} += "xyz \\
                                                 zzz"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS:class-native += "\\
                                         rubygems-mini-portile2-native \\
                                         rubygems-racc-native \\
                                     "
                                     DEPENDS:class-target += "\\
                                         rubygems-mini-portile2 \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "a (>= 1.2.3) \\
                                                 b (>= 4.5.6)"
                                     ''',
                                 },
                                 {
                                     'recipes/oelint_adv_test.bb':
                                     '''
                                     DEPENDS:append = " z"
                                     inherit foo
                                     ''',
                                     'conf/layer.conf':
                                     ' ',
                                     'classes/foo.bbclass':
                                     'DEPENDS:append = " a"',
                                 },
                                 {
                                     'recipes/oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN}:append = " z"
                                     inherit foo
                                     ''',
                                     'conf/layer.conf':
                                     ' ',
                                     'classes/foo.bbclass':
                                     'RDEPENDS:${PN}:append = " a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "abc def ghi"
                                     DEPENDS:remove = "def"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} += "abc def ghi"
                                     RDEPENDS:${PN}:remove = "def"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} = "x y z"
                                     RDEPENDS:${PN}:append:magic-machine = " a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} = "x y z"
                                     RDEPENDS:${PN}:prepend:magic-machine = "a "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS_${PN} += "\\
                                        bash \\
                                        libFormatConversion.so()(64bit) \\
                                        libMvCameraControl.so()(64bit) \\
                                        libMVRender.so()(64bit) \\
                                        libstdc++ \\
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
