import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass


class TestClassOelintVarMandatoryVar(TestBaseClass):

    def __generate_sample_code(self, var, extra):
        return '''
            {extra}
            {var} = "foo"
            '''.format(var=var, extra=extra)

    @pytest.mark.parametrize('id', ['oelint.var.mandatoryvar'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        "SUMMARY",
        "DESCRIPTION",
        "HOMEPAGE",
        "LICENSE",
        "SRC_URI"
    ])
    def test_bad(self, id, occurrence, var):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code('A', '')
        }
        id += '.{}'.format(var)
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', ['oelint.var.mandatoryvar'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        "SUMMARY",
        "DESCRIPTION",
        "LICENSE"
    ])
    @pytest.mark.parametrize('extra', [
        'IMAGE_INSTALL_append = " foo"',
        'inherit image',
        'inherit core-image',
        'IMAGE_INSTALL += " foo"',
        'IMAGE_INSTALL = "foo"'
    ])
    def test_bad_image(self, id, occurrence, var, extra):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code('A', extra)
        }
        id += '.{}'.format(var)
        self.check_for_id(self._create_args(input), id, occurrence)

    @pytest.mark.parametrize('id', [
        'oelint.var.mandatoryvar.SUMMARY',
        'oelint.var.mandatoryvar.DESCRIPTION',
        'oelint.var.mandatoryvar.HOMEPAGE',
        'oelint.var.mandatoryvar.LICENSE',
        'oelint.var.mandatoryvar.SRC_URI',
        ])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            SUMMARY = "foo"
            DESCRIPTION = "foo"
            HOMEPAGE = "foo"
            LICENSE = "foo"
            SRC_URI = "foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit core-image
            SUMMARY = "foo"
            DESCRIPTION = "foo"
            LICENSE = "foo"
            '''
            },
            {
            'oelint_adv_test.bb':
            '''
            inherit image
            SUMMARY = "foo"
            DESCRIPTION = "foo"
            LICENSE = "foo"
            '''
            },
                        {
            'oelint_adv_test.bb':
            '''
            inherit packagegroup
            SUMMARY = "foo"
            DESCRIPTION = "foo"
            '''
            },
        ],
    )
    def test_good(self, input, id, occurrence):
        self.check_for_id(self._create_args(input), id, occurrence)


 
