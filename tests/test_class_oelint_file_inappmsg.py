import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintFileUpstreamStatusInAppMsg(TestBaseClass):

    def _generate_input(patch_suffix, upstream_status):
        return {
            'oelint_adv-test.bb': f'SRC_URI = "file://test.{patch_suffix}"',
            f'files/test.{patch_suffix}': f'Upstream-Status: {upstream_status}',
        }

    @pytest.mark.parametrize('id_', ['oelint.file.inappropriatemsg'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Inappropriate [me don\'t care]'),
                                 _generate_input('diff', 'Inappropriate [me don\'t care]'),
                                 _generate_input('patch', 'Inappropriate'),
                                 _generate_input('diff', 'Inappropriate'),
                                 _generate_input('patch', 'Inappropriate (configuration)'),
                                 _generate_input('diff', 'Inappropriate (configuration)'),
                              ],
                             )
    def test_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.inappropriatemsg'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Inappropriate [oe-specific]'),
                                 _generate_input('diff', 'Inappropriate [oe-specific]'),
                                 _generate_input('patch', 'Inappropriate [OE specific]'),
                                 _generate_input('diff', 'Inappropriate [OE specific]'),
                                 _generate_input('patch', 'Inappropriate [oe-core specific]'),
                                 _generate_input('diff', 'Inappropriate [oe-core specific]'),
                                 _generate_input('patch', 'Inappropriate [not author]'),
                                 _generate_input('diff', 'Inappropriate [not author]'),
                                 _generate_input('patch', 'Inappropriate [native]'),
                                 _generate_input('diff', 'Inappropriate [native]'),
                                 _generate_input('patch', 'Inappropriate [licensing]'),
                                 _generate_input('diff', 'Inappropriate [licensing]'),
                                 _generate_input('patch', 'Inappropriate [configuration]'),
                                 _generate_input('diff', 'Inappropriate [configuration]'),
                                 _generate_input('patch', 'Inappropriate [enable feature]'),
                                 _generate_input('diff', 'Inappropriate [enable feature]'),
                                 _generate_input('patch', 'Inappropriate [disable feature]'),
                                 _generate_input('diff', 'Inappropriate [disable feature]'),
                                 _generate_input('patch', 'Inappropriate [bugfix this and that]'),
                                 _generate_input('diff', 'Inappropriate [bugfix this and that]'),
                                 _generate_input('patch', 'Inappropriate [bugfix #12345]'),
                                 _generate_input('diff', 'Inappropriate [bugfix #12345]'),
                                 _generate_input('patch', 'Inappropriate [embedded specific]'),
                                 _generate_input('diff', 'Inappropriate [embedded specific]'),
                                 _generate_input('patch', 'Inappropriate [no upstream]'),
                                 _generate_input('diff', 'Inappropriate [no upstream]'),
                                 _generate_input('patch', 'Inappropriate [other]'),
                                 _generate_input('diff', 'Inappropriate [other]'),
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.patch"',
                                     'files/test.patch':
                                     '''
                                     Some line before
                                     Upstream-Status: Inappropriate [other]
                                     Some line after
                                     ''',
                                 },
                                 {
                                     'oelint_adv-test.bb':
                                     'SRC_URI = "file://test.diff"',
                                     'files/test.diff':
                                     '''
                                     Some line before
                                     Upstream-Status: Inappropriate [other]
                                     Some line after
                                     ''',
                                 },
                             ],
                             )
    def test_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
