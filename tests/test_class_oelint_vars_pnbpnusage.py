import pytest
from base import TestBaseClass


class TestClassOelintVarsPNBPNUsage(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.pnbpnusage'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "file://${PN}.patch"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "git://${PN}.com/${PN}.git"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "https://foo.org/${PN}"
            '''
            },
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.pnbpnusage'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "file://${BPN}.patch"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "git://${BPN}.com/${BPN}.git"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "https://foo.org/${BPN}"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            S = "${WORDKIR}/${BPN}"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "git://foo.org/baz.git;name=${PN}-super"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            SRC_URI = "git://foo.org/${BPN}.git;name=${PN}-ultra"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
