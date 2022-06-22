import pytest

from .base import TestBaseClass


# flake8: noqa S101 - n.a. for test files
class TestClassInlineSuppressions(TestBaseClass):

    @pytest.mark.parametrize('input',
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
    def test_inlinesuppressions_single(self, input):
        self.check_for_id(self._create_args(input),
                          'oelint.vars.insaneskip', 0)

    @pytest.mark.parametrize('input',
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
    def test_inlinesuppressions_single_notmatching(self, input):
        self.check_for_id(self._create_args(input),
                          'oelint.vars.insaneskip', 1)

    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint adv-test.bb':
                                     '''
                                    # nooelint: oelint.var.suggestedvar.BUGTRACKER,oelint.var.mandatoryvar.SUMMARY,oelint.var.bbclassextend
                                    INSANE_SKIP_${PN} = "foo"
                                    ''',
                                 }
                             ],
                             )
    def test_inlinesuppressions_line_1(self, input):
        self.check_for_id(self._create_args(input),
                          'oelint.var.suggestedvar.BUGTRACKER', 0)
        self.check_for_id(self._create_args(input),
                          'oelint.var.mandatoryvar.SUMMARY', 0)
        self.check_for_id(self._create_args(input),
                          'oelint.var.bbclassextend', 0)

    @pytest.mark.parametrize('input',
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
    def test_inlinesuppressions_multiple(self, input):
        self.check_for_id(self._create_args(input), 'oelint.vars.specific', 0)
        self.check_for_id(self._create_args(input),
                          'oelint.vars.doublemodify', 0)
        self.check_for_id(self._create_args(input),
                          'oelint.vars.overrideappend', 0)

    @pytest.mark.parametrize('input',
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
    def test_inlinesuppressions_multiple_scope(self, input):
        self.check_for_id(self._create_args(input), 'oelint.vars.specific', 1)
        self.check_for_id(self._create_args(input),
                          'oelint.vars.doublemodify', 1)
        self.check_for_id(self._create_args(input),
                          'oelint.vars.overrideappend', 1)
