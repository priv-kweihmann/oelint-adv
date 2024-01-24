import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsVirtual(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.virtual'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RDEPENDS:${PN} = "virtual/a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     RPROVIDES:${PN} = "virtual/a"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     require something.inc
                                     RDEPENDS:${PN}-doc = "abc def virtual/a"
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
                                     'RDEPENDS:${PN} += "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN}:append = "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RPROVIDES:${PN} += "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RPROVIDES:${PN}:append = "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN}:remove = "virtual/a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RPROVIDES:${PN}:remove = "virtual/a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RPROVIDES:${PN} += "virtual-reality"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'RPROVIDES:${PN}:append = "virtual-reality"',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
