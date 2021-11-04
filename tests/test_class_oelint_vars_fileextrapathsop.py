import pytest
from .base import TestBaseClass


class TestClassOelintVarsFilextrapaths(TestBaseClass):

    @pytest.mark.parametrize('id', ['oelint.vars.fileextrapathsop'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            FILESEXTRAPATHS_prepend .= "${THISDIR}/file"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILESEXTRAPATHS_append = "${THISDIR}/file"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILESEXTRAPATHS += "${THISDIR}/file"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILESEXTRAPATHS =. "${THISDIR}/file"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            FILESEXTRAPATHS .= "${THISDIR}/file"
            '''
            }
            ,
            {
            'oelint_adv_test.bb':
            '''
            FILESEXTRAPATHS =+ "${THISDIR}/file"
            '''
            }
        ],
    )
    def test_bad(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.vars.fileextrapathsop'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bbappend':
            '''
            FILESEXTRAPATHS_prepend := "${THISDIR}/file"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILESEXTRAPATHS_append := "${THISDIR}/file"
            '''
            },
            {
            'oelint_adv_test.bbappend':
            '''
            FILESEXTRAPATHS := "${THISDIR}/file"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)
