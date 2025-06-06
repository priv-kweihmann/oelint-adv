import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintTaskHeredocs(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.task.heredocs'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_foo() {
                                         cat    >  ${T}/some.files <<   abchhehdhhe
                                         kfkdfkd
                                         abchhehdhhe
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install_append() {
                                         cat    <<   EOF    >${T}/some.files
                                         abc
                                         EOF
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.heredocs'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install() {
                                         abc
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     # nooelint: oelint.task.heredocs
                                     do_install:append() {
                                        some operation
                                        cat    <<   EOF    >${T}/some.files
                                        abc
                                        EOF
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
