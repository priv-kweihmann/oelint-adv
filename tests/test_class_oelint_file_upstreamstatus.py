import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintFileUpstreamStatus(TestBaseClass):

    def _generate_input(patch_suffix, upstream_status):
        return {
            'oelint_adv-test.bb': f'SRC_URI = "file://test.{patch_suffix}"',
            f'files/test.{patch_suffix}': f'Upstream-Status: {upstream_status}',
        }

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.patch"',
                                     'files/test.patch':
                                     'This is not a patch',
                                 },
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.diff"',
                                     'files/test.diff':
                                     'This is not a patch',
                                 },
                                 _generate_input('patch', 'Acceppted'),
                                 _generate_input('diff', 'Acceppted'),
                                 _generate_input('patch', 'Submit'),
                                 _generate_input('diff', 'Submit'),
                                 _generate_input('patch', 'Inapropriate'),
                                 _generate_input('diff', 'Inapropriate'),
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Accepted'),
                                 _generate_input('diff', 'Accepted'),
                                 _generate_input('patch', 'Backport'),
                                 _generate_input('diff', 'Backport'),
                                 _generate_input('patch', 'Denied'),
                                 _generate_input('diff', 'Denied'),
                                 _generate_input('patch', 'Inappropriate [bugfix this is a bugfix]'),
                                 _generate_input('diff', 'Inappropriate [bugfix this is a bugfix]'),
                                 _generate_input('patch', 'Inappropriate [configuration]'),
                                 _generate_input('diff', 'Inappropriate [configuration]'),
                                 _generate_input('patch', 'Inappropriate [disable feature]'),
                                 _generate_input('diff', 'Inappropriate [disable feature]'),
                                 _generate_input('patch', 'Inappropriate'),
                                 _generate_input('diff', 'Inappropriate'),
                                 _generate_input('patch', 'Inappropriate [embedded specific]'),
                                 _generate_input('diff', 'Inappropriate [embedded specific]'),
                                 _generate_input('patch', 'Inappropriate [enable feature]'),
                                 _generate_input('diff', 'Inappropriate [enable feature]'),
                                 _generate_input('patch', 'Inappropriate [licensing]'),
                                 _generate_input('diff', 'Inappropriate [licensing]'),
                                 _generate_input('patch', 'Inappropriate [native]'),
                                 _generate_input('diff', 'Inappropriate [native]'),
                                 _generate_input('patch', 'Inappropriate [no upstream]'),
                                 _generate_input('diff', 'Inappropriate [no upstream]'),
                                 _generate_input('patch', 'Inappropriate [other]'),
                                 _generate_input('diff', 'Inappropriate [other]'),
                                 _generate_input('patch', 'Pending'),
                                 _generate_input('diff', 'Pending'),
                                 _generate_input('patch', 'Submitted [http://some.where]'),
                                 _generate_input('diff', 'Submitted [http://some.where]'),
                                 _generate_input('patch', 'Inactive-Upstream'),
                                 _generate_input('diff', 'Inactive-Upstream'),
                                 _generate_input('patch', 'Inactive-Upstream [lastcommit 1234]'),
                                 _generate_input('diff', 'Inactive-Upstream [lastcommit 1234]'),
                                 _generate_input('patch', 'Inactive-Upstream [lastrelease 1234]'),
                                 _generate_input('diff', 'Inactive-Upstream [lastrelease 1234]'),
                                 _generate_input('patch', 'Inactive-Upstream [lastcommit 1234 lastrelease 1234]'),
                                 _generate_input('diff', 'Inactive-Upstream [lastcommit 1234 lastrelease 1234]'),
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.patch"',
                                     'files/test.patch':
                                     '''
                                     Some line before that
                                     Upstream-Status: Inappropriate
                                     Some line after that
                                     ''',
                                 },
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.diff"',
                                     'files/test.diff':
                                     '''
                                     Some line before that
                                     Upstream-Status: Inappropriate
                                     Some line after that
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
