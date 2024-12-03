import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintFileUnderscores(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.file.underscores'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test-1.2.3.bb':
                                     'VAR = "1"',
                                 },
                                 {
                                     'oelintadvtest.bb':
                                     'VAR = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'VAR = "1"',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.underscores'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv-test.bb':
                                     'VAR = "1"',
                                 },
                                 {
                                     'oelint-adv_test-1.2.3.bb':
                                     'VAR = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit core-image',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit image',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'IMAGE_INSTALL += "foo"',
                                 },
                                 {
                                     'oelint-adv_1.2.3.bb':
                                     'VAR = "a"',
                                 },
                                 {
                                     'oelint-adv_git.bb':
                                     'VAR = "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit packagegroup',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.underscores'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'inherit my-image',
                                 },
                             ],
                             )
    def test_good_image_mod(self, input_, id_, occurrence):
        __cnt = '''
        {
            "images": {
                "known-classes": [
                    "my-image"
                ]
            },
            "functions": {
                "order": ["do_foo"]
            }
        }
        '''
        _extra_opts = [
            '--constantmods=+{mod}'.format(mod=self._create_tempfile('constmod', __cnt))]
        _args = self._create_args(input_, extraopts=_extra_opts)

        self.check_for_id(_args, id, occurrence)
