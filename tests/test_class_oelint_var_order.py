import pytest  # noqa: I900

from .base import TestBaseClass

VAR_ORDER = [
    'SUMMARY',
    'DESCRIPTION',
    'AUTHOR',
    'HOMEPAGE',
    'BUGTRACKER',
    'SECTION',
    'LICENSE',
    'LIC_FILES_CHKSUM',
    'DEPENDS',
    'PROVIDES',
    'PV',
    'SRC_URI',
    'SRCREV',
    'S',
    'inherit',
    'PACKAGECONFIG',
    'EXTRA_QMAKEVARS_POST',
    'EXTRA_OECONF',
    'PACKAGE_ARCH',
    'PACKAGES',
    'FILES_${PN}',
    'RDEPENDS_${PN}',
    'RRECOMMENDS_${PN}',
    'RSUGGESTS_${PN}',
    'RPROVIDES_${PN}',
    'RCONFLICTS_${PN}',
    'BBCLASSEXTEND',
]


class TestClassOelintVarOrder(TestBaseClass):

    def __generate_sample_code(self, first, second):
        return '''
            {first} = "foo"
            {second} = "foo"
            '''.format(first=first, second=second)

    @pytest.mark.parametrize('id_', ['oelint.var.order'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', VAR_ORDER)
    def test_bad(self, id_, occurrence, var):
        try:
            id_ += '.{var}'.format(var=var)
            for item in VAR_ORDER[:VAR_ORDER.index(var)]:
                input_ = {
                    'oelint_adv_test.bb': self.__generate_sample_code(item, var),
                }
                self.check_for_id(self._create_args(input_), id_, occurrence)
        except Exception:  # noqa: S110
            pass

    @pytest.mark.parametrize('id_', ['oelint.var.order'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', VAR_ORDER)
    def test_good(self, id_, occurrence, var):
        try:
            id_ += '.{var}'.format(var=var)
            for item in VAR_ORDER[VAR_ORDER.index(var):]:
                input_ = {
                    'oelint_adv_test.bb': self.__generate_sample_code(item, var),
                }
                self.check_for_id(self._create_args(input_), id_, occurrence)
        except Exception:  # noqa: S110
            pass

    @pytest.mark.parametrize('id_', ['oelint.var.order.SRCREV'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.inc':
                                     '''
                                     SUMMARY = "..."
                                     DESCRIPTION = "...
                                     AUTHOR = "..."
                                     HOMEPAGE = "..."
                                     BUGTRACKER = "..."
                                     BBCLASSEXTEND += "nativesdk"
                                     ''',
                                     'oelint_adv_test.bb':
                                     '''
                                     require oelint_adv_test.inc
                                     SRCREV = "..."
                                     ''',
                                 },
                             ],
                             )
    def test_single_file_scope(self, id_, occurrence, input_):
        self.check_for_id(self._create_args(input_), id_, occurrence)
