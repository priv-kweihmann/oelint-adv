import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarMultiInherit(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.var.multiinherit'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit abc abc',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit def
                                     inherit ghi def
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.multiinherit'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit abc def
                                     inherit autotools \\
                                             gobject-introspection \\
                                             pkgconfig
                                     ''',
                                 },
                                 {
                                     'classes/d.class': '',
                                     'classes/c.class': 'inherit d',
                                     'classes/b.class': 'inherit d',
                                     'classes/a.class': 'inherit d',
                                     'conf/layer.conf': '',
                                     'oelint_adv_test.bb': 'inherit a b c',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
