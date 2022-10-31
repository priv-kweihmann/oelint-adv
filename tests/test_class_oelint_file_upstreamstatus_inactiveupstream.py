import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintFileUpstreamStatusInactiveUpstreamDetails(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.file.inactiveupstreamdetails'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.patch"',
                                     'files/test.patch':
                                     'Upstream-Status: Inactive-Upstream',
                                 },
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.patch"',
                                     'files/test.patch':
                                     'Upstream-Status: Inactive-Upstream [1234]',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.inactiveupstreamdetails'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.patch"',
                                     'files/test.patch':
                                     'Upstream-Status: Inactive-Upstream [lastcommit 1234]',
                                 },
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.patch"',
                                     'files/test.patch':
                                     'Upstream-Status: Inactive-Upstream [lastrelease 1234]',
                                 },
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.patch"',
                                     'files/test.patch':
                                     'Upstream-Status: Inactive-Upstream [lastcommit 1234 lastrelease 1234]',
                                 },
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
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
