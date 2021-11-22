import pytest

from .base import TestBaseClass


class TestClassOelintVarsDuplicate(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.duplicate'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input',
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
                             ],
                             )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.duplicate'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input',
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
                             ],
                             )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
