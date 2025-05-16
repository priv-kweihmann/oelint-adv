import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsMispell(TestBaseClass):

    @pytest.mark.parametrize('id_', ['oelint.vars.mispell'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'DPENDS += "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'FILS = "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRR_URI[sha256sum] = "1234"',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     BBFILE_PATTERN_fooo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     BBFILE_PRIORITY_fooo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     LAYERVERSION_fooo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     LAYERDEPENDS_fooo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     LAYERSERIES_COMPAT_fooo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     LAYERRECOMMENDS_fooo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     BBFILE_PATTERN_IGNORE_EMPTY_fooo += ""
                                     ''',
                                 },
                             ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.mispell.unknown'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'A += "foo"',
                                 },
                             ],
                             )
    def test_bad_unknown(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.mispell'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS:${PN} = "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'PACKAGECONFIG[foo] = "a"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '_SECRETVAR = "1"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     PACKAGECONFIG_A = "a"
                                     PACKAGECONFIG_B = "c"
                                     do_configure() {
                                         ./configure ${PACKAGECONFIG_A}
                                     }
                                     python do_foo() {
                                         d.getVar("PACKAGECONFIG_B")
                                     }
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     PACKAGES += "${PN}-foo"
                                     INITSCRIPT_PARAMS:${PN}-foo = "bar"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     DEPENDS:qemux86 = "something"

                                     SRC_URI = "git://github.com/znc/znc.git;name=znc;branch=master;protocol=https \\
                                                git://github.com/jimloco/Csocket.git;destsuffix=git/third_party/Csocket;name=Csocket;branch=master;protocol=https"
                                     SRCREV_znc = "bf253640d33d03331310778e001fb6f5aba2989e"
                                     SRCREV_Csocket = "e8d9e0bb248c521c2c7fa01e1c6a116d929c41b4"

                                     ''',
                                 },
                                 {
                                     'abc.bb':
                                     '''
                                     DEPENDS:qemux86 = "something"

                                     SRC_URI = "git://github.com/znc/znc.git;name=abc;branch=master;protocol=https \\
                                                git://github.com/jimloco/Csocket.git;destsuffix=git/third_party/Csocket;name=Csocket;branch=master;protocol=https"
                                     SRCREV_abc = "bf253640d33d03331310778e001fb6f5aba2989e"
                                     SRCREV_Csocket = "e8d9e0bb248c521c2c7fa01e1c6a116d929c41b4"
                                     ''',
                                 },
                                 {
                                     'abc.bb':
                                     '''
                                     SRC_URI = "git://github.com/znc/znc.git;name=abc;branch=master;protocol=https \\
                                                git://github.com/jimloco/Csocket.git;destsuffix=git/third_party/Csocket;name=Csocket;branch=master;protocol=https"
                                     SRCREV_Csocket[doc] = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_install[prefuncs] += "foo"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '_do_secret[prefuncs] += "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     dskfdsfkjfhsjkfsdjfkj = "1"
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     BBFILE_PATTERN_foo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     BBFILE_PRIORITY_foo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     LAYERVERSION_foo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     LAYERDEPENDS_foo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     LAYERSERIES_COMPAT_foo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     LAYERRECOMMENDS_foo += ""
                                     ''',
                                 },
                                 {
                                     'conf/layer.conf':
                                     '''
                                     BBFILE_COLLECTIONS += "foo"
                                     BBFILE_PATTERN_IGNORE_EMPTY_foo += ""
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.mispell'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'RDEPENDS_${PN} = "foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     PACKAGES += "${PN}-foo"
                                     INITSCRIPT_PARAMS_${PN}-foo = "bar"
                                     ''',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '_SECRETVAR = "1"',
                                 },
                             ],
                             )
    def test_good_old(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.mispell.unknown'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     A = "a"
                                     B = "c"
                                     do_configure() {
                                         ./configure ${A}
                                     }
                                     python do_foo() {
                                         d.getVar("B")
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good_unknown(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
