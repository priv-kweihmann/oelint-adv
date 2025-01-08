import pytest  # noqa: I900

from .base import TestBaseClass


# flake8: noqa S101 - n.a. for test files
class TestClassInlineSuppressions(TestBaseClass):

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     # nooelint: oelint.vars.insaneskip
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     #   nooelint: oelint.vars.insaneskip
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     # nooelint:    oelint.vars.insaneskip
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 },
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     # nooelint: oelint.vars.insaneskip - some explanation
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 }
                             ],
                             )
    def test_inlinesuppressions_single(self, input_):
        self.check_for_id(self._create_args(input_),
                          'oelint.vars.insaneskip', 0)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     # nooelint: oelint.vars.someother
                                     INSANE_SKIP:${PN} = "foo"
                                     ''',
                                 }
                             ],
                             )
    def test_inlinesuppressions_single_notmatching(self, input_):
        self.check_for_id(self._create_args(input_),
                          'oelint.vars.insaneskip', 1)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     # nooelint: oelint.vars.someother
                                     INSANE_SKIP_${PN} = "foo"
                                     ''',
                                 }
                             ],
                             )
    def test_inlinesuppressions_single_notmatching_old(self, input_):
        self.check_for_id(self._create_args(input_, ['--release=dunfell']),
                          'oelint.vars.insaneskip', 1)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                    # nooelint: oelint.var.suggestedvar.BUGTRACKER,oelint.var.mandatoryvar.SUMMARY,oelint.var.bbclassextend
                                    INSANE_SKIP_${PN} = "foo"
                                    ''',
                                 },
                             ],
                             )
    def test_inlinesuppressions_line_1(self, input_):
        self.check_for_id(self._create_args(input_),
                          'oelint.var.suggestedvar.BUGTRACKER', 0)
        self.check_for_id(self._create_args(input_),
                          'oelint.var.mandatoryvar.SUMMARY', 0)
        self.check_for_id(self._create_args(input_),
                          'oelint.var.bbclassextend', 0)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     # nooelint: oelint.var.badimagefeature.allow-empty-password,oelint.var.badimagefeature.allow-root-login,oelint.var.badimagefeature.empty-root-password
                                     IMAGE_FEATURES:append = " \
                                        allow-empty-password allow-root-login empty-root-password \
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_inlinesuppressions_line_2(self, input_):
        self.check_for_id(self._create_args(input_),
                          'oelint.var.badimagefeature', 0)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                A = "1"
                                # nooelint: oelint.vars.specific,oelint.vars.doublemodify,oelint.vars.overrideappend
                                SOMEUNKNOWN_VAR:unknown-override:append += "foo"
                                ''',
                                 }
                             ],
                             )
    def test_inlinesuppressions_multiple(self, input_):
        self.check_for_id(self._create_args(input_), 'oelint.vars.specific', 0)
        self.check_for_id(self._create_args(input_),
                          'oelint.vars.doublemodify', 0)
        self.check_for_id(self._create_args(input_),
                          'oelint.vars.overrideappend', 0)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                            SOMEUNKNOWN_VAR:unknown-override:append += "foo"
                            # nooelint: oelint.vars.specific,oelint.vars.doublemodify,oelint.vars.overrideappend
                            SOMEOTHER_VAR:unknown-override:append += "foo"
                            ''',
                                 }
                             ],
                             )
    def test_inlinesuppressions_multiple_scope(self, input_):
        self.check_for_id(self._create_args(input_), 'oelint.vars.specific', 1)
        self.check_for_id(self._create_args(input_),
                          'oelint.vars.doublemodify', 1)
        self.check_for_id(self._create_args(input_),
                          'oelint.vars.overrideappend', 1)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     # nooelint: oelint.var.badimagefeature.allow-empty-password,,oelint.var.badimagefeature.allow-root-login,oelint.var.badimagefeature.empty-root-password
                                     IMAGE_FEATURES:append = " \
                                        allow-empty-password allow-root-login empty-root-password \
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_inlinesuppressions_remove_empty(self, input_):
        self.check_for_id(self._create_args(input_),
                          'oelint.var.badimagefeature', 0)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                     # nooelint: oelint.var.badimagefeature.allow-empty-password - this is a comment
                                     IMAGE_FEATURES:append = " \
                                        allow-empty-password \
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_inlinesuppressions_with_comment(self, input_):
        self.check_for_id(self._create_args(input_),
                          'oelint.var.badimagefeature', 0)
