import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintFileUpstreamStatusInactiveUpstreamDetails(TestBaseClass):

    def _generate_input(patch_suffix, upstream_status):
        return {
            'oelint_adv-test.bb': f'SRC_URI = "file://test.{patch_suffix}"',
            f'files/test.{patch_suffix}': f'Upstream-Status: {upstream_status}',
        }

    @pytest.mark.parametrize('id_', ['oelint.file.inactiveupstreamdetails'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Inactive-Upstream'),
                                 _generate_input('diff', 'Inactive-Upstream'),
                                 _generate_input('patch', 'Inactive-Upstream [1234]'),
                                 _generate_input('diff', 'Inactive-Upstream [1234]'),
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.inactiveupstreamdetails'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
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
                                     Some line before
                                     Upstream-Status: Inactive-Upstream [lastcommit 1234 lastrelease 1234]
                                     Some line after
                                     ''',
                                 },
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.diff"',
                                     'files/test.diff':
                                     '''
                                     Some line before
                                     Upstream-Status: Inactive-Upstream [lastcommit 1234 lastrelease 1234]
                                     Some line after
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
