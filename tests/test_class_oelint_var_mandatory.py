import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarMandatoryVar(TestBaseClass):

    def __generate_sample_code(self, var, extra):
        return '''
            {extra}
            {var} = "foo"
            '''.format(var=var, extra=extra)

    @pytest.mark.parametrize('id_', ['oelint.var.mandatoryvar'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'SUMMARY',
        'DESCRIPTION',
        'HOMEPAGE',
        'LICENSE',
        'SRC_URI',
    ])
    def test_bad(self, id_, occurrence, var):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code('A', ''),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.var.mandatoryvar'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'SUMMARY',
        'DESCRIPTION',
        'LICENSE',
    ])
    @pytest.mark.parametrize('extra', [
        'IMAGE_INSTALL_append = " foo"',
        'inherit image',
        'inherit core-image',
        'IMAGE_INSTALL += " foo"',
        'IMAGE_INSTALL = "foo"',
    ])
    def test_bad_image(self, id_, occurrence, var, extra):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code('A', extra),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', [
        'oelint.var.mandatoryvar.SUMMARY',
        'oelint.var.mandatoryvar.DESCRIPTION',
        'oelint.var.mandatoryvar.HOMEPAGE',
        'oelint.var.mandatoryvar.LICENSE',
        'oelint.var.mandatoryvar.SRC_URI',
    ])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SUMMARY = "foo"
                                     DESCRIPTION = "foo"
                                     HOMEPAGE = "foo"
                                     LICENSE = "foo"
                                     SRC_URI = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit core-image
                                     SUMMARY = "foo"
                                     DESCRIPTION = "foo"
                                     LICENSE = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit image
                                     SUMMARY = "foo"
                                     DESCRIPTION = "foo"
                                     LICENSE = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     inherit packagegroup
                                     SUMMARY = "foo"
                                     DESCRIPTION = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SUMMARY = "foo"
                                     DESCRIPTION = "foo"
                                     HOMEPAGE = "foo"
                                     LICENSE = "foo"
                                     inherit pypi
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SUMMARY = "foo"
                                     DESCRIPTION = "foo"
                                     HOMEPAGE = "foo"
                                     LICENSE = "foo"
                                     inherit gnomebase
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', [
        'oelint.var.mandatoryvar.SRC_URI',
    ])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     SUMMARY = "foo"
                                     DESCRIPTION = "foo"
                                     LICENSE = "foo"
                                     inherit foo
                                     ''',
                                 },
                             ],
                             )
    def test_good_custom_varname_class(self, input_, id_, occurrence):
        __cnt = '''
        {
            "oelint-mandatoryvar": {
                "SRC_URI-exclude-classes": [
                    "foo"
                ],
                "HOMEPAGE-exclude-classes": [
                    "foo"
                ]
            }
        }
        '''
        _extra_opts = [
            '--constantmod=+{mod}'.format(mod=self._create_tempfile('constmod', __cnt))]
        self.check_for_id(self._create_args(input_, _extra_opts), id_, occurrence)
