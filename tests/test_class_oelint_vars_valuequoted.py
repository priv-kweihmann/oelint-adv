import pytest  # noqa: I900

from .base import TestBaseClass

# flake8: noqa W291 - we want to explicitly test trailing whitespace here
class TestClassOelintVarsValueQuoted(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.valuequoted'])
    @pytest.mark.parametrize('occurrence', [2])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "a
                                     D = a"
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.valuequoted'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'A = "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'A += "b"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'PACKAGECONFIG[foo] = "-DFOO=ON,-DFOO=OFF,"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'EXTRA_OEMAKE = \'CROSS_COMPILE=${TARGET_PREFIX} CC="${TARGET_PREFIX}gcc ${TOOLCHAIN_OPTIONS}" V=1\'',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     EXTRA_OECMAKE += "\\
                                         -DBUILD_TESTS=OFF \\
                                     "
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS += "\\
                                     a \\
                                     b \\    
                                     c \\
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
