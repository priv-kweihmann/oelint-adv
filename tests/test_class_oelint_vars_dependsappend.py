import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsDependsAppend(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.dependsappend'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit something
                                     DEPENDS = "bar"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     include something.inc
                                     DEPENDS = "bar"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     require something.inc
                                     DEPENDS = "bar"
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
                                     'DEPENDS += "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS_prepend =  "baz "',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS_append = " xyz"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'DEPENDS_remove = "abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS = "foo"
                                     inherit something
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS = "foo"
                                     include something.inc
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS = "foo"
                                     require something.inc
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
