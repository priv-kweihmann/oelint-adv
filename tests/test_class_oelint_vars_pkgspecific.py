import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassOelintVarsPKGSpecific(TestBaseClass):

    def __generate_sample_code(self, var):
        return '''
            {var} = "foo"
            '''.format(var=var)

    @pytest.mark.parametrize('id', ['oelint.vars.pkgspecific'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('var', [
        "RDEPENDS",
        "RRECOMMENDS",
        "RSUGGESTS",
        "RCONFLICTS",
        "RPROVIDES",
        "RREPLACES",
        "FILES",
        "pkg_preinst",
        "pkg_postinst",
        "pkg_prerm",
        "pkg_postrm",
        "ALLOW_EMPTY",
    ])
    def test_bad(self, id, occurance, var):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(var)
        }
        id += '.{}'.format(var)
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.vars.pkgspecific'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('var', [
        "RDEPENDS_${PN}",
        "RRECOMMENDS_${PN}",
        "RSUGGESTS_${PN}",
        "RCONFLICTS_${PN}",
        "RPROVIDES_${PN}",
        "RREPLACES_${PN}",
        "FILES_${PN}",
        "pkg_preinst_${PN}",
        "pkg_postinst_${PN}",
        "pkg_prerm_${PN}",
        "pkg_postrm_${PN}",
        "ALLOW_EMPTY_${PN}",
    ])
    def test_good(self, id, occurance, var):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(var)
        }
        id += '.{}'.format(var)
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', [
        'oelint.var.pkgspecific.RDEPENDS',
        'oelint.var.pkgspecific.RRECOMMENDS',
        'oelint.var.pkgspecific.RSUGGESTS',
        'oelint.var.pkgspecific.RCONFLICTS',
        'oelint.var.pkgspecific.RPROVIDES',
        'oelint.var.pkgspecific.RREPLACES',
        'oelint.var.pkgspecific.FILES',
        'oelint.var.pkgspecific.pkg_preinst',
        'oelint.var.pkgspecific.pkg_postinst',
        'oelint.var.pkgspecific.pkg_prerm',
        'oelint.var.pkgspecific.pkg_postrm',
        'oelint.var.pkgspecific.ALLOW_EMPTY',
        ])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
        [
            {
            'oelint_adv_test.bb':
            '''
            PACKAGES += "abc-foo"
            RDEPENDS_abc-foo += "bar"
            '''
            },
        ],
    )
    def test_good_custom_pkg(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)


 
