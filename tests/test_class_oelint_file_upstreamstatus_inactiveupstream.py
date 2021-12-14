import pytest

from .base import TestBaseClass


class TestClassOelintFileUpstreamStatusInactiveUpstreamDetails(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.file.inactiveupstreamdetails'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input',
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
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.file.inactiveupstreamdetails'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input',
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
                             ],
                             )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
