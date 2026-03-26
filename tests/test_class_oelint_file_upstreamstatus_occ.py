import json

import pytest  # noqa: I900

from .base import TestBaseClass

class TestClassOelintFileUpstreamStatusOcc(TestBaseClass):

    def _generate_input(patch_suffix, upstream_status):
        return {
            'oelint_adv-test.bb': f'SRC_URI = "file://test.{patch_suffix}"',
            f'files/test.{patch_suffix}': f'Upstream-Status: {upstream_status}',
        }

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Pending'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Pending'),
                                 _generate_input('diff', 'Pending')
                             ],
                             )
    def test_pending(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Pending'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Pending'),
                                 _generate_input('diff', 'Pending')
                             ],
                             )
    def test_pending_std(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Pending'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'SomethingElse'),
                                 _generate_input('diff', 'SomethingElse')
                             ],
                             )
    def test_pending_no_hit(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Submitted'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Submitted'),
                                 _generate_input('diff', 'Submitted')
                             ],
                             )
    def test_submitted(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Submitted'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Submitted'),
                                 _generate_input('diff', 'Submitted')
                             ],
                             )
    def test_submitted_std(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Submitted'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'SomethingElse'),
                                 _generate_input('diff', 'SomethingElse')
                             ],
                             )
    def test_submitted_no_hit(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Accepted'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Accepted'),
                                 _generate_input('diff', 'Accepted')
                             ],
                             )
    def test_accepted(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Accepted'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Accepted'),
                                 _generate_input('diff', 'Accepted')
                             ],
                             )
    def test_accepted_std(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Accepted'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'SomethingElse'),
                                 _generate_input('diff', 'SomethingElse')
                             ],
                             )
    def test_accepted_no_hit(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Denied'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Denied'),
                                 _generate_input('diff', 'Denied')
                             ],
                             )
    def test_denied(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Denied'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Denied'),
                                 _generate_input('diff', 'Denied')
                             ],
                             )
    def test_denied_std(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Denied'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'SomethingElse'),
                                 _generate_input('diff', 'SomethingElse')
                             ],
                             )
    def test_denied_no_hit(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Backport'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Backport'),
                                 _generate_input('diff', 'Backport')
                             ],
                             )
    def test_backport(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Backport'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Backport'),
                                 _generate_input('diff', 'Backport')
                             ],
                             )
    def test_backport_std(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Backport'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'SomethingElse'),
                                 _generate_input('diff', 'SomethingElse')
                             ],
                             )
    def test_backport_no_hit(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Inappropriate'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Inappropriate [foo]'),
                                 _generate_input('diff', 'Inappropriate [foo]')
                             ],
                             )
    def test_inappropriate(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Inappropriate'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Inappropriate [foo]'),
                                 _generate_input('diff', 'Inappropriate [foo]')
                             ],
                             )
    def test_inappropriate_std(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Inappropriate'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'SomethingElse'),
                                 _generate_input('diff', 'SomethingElse')
                             ],
                             )
    def test_inappropriate_no_hit(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Inactive-Upstream'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Inactive-Upstream [foo]'),
                                 _generate_input('diff', 'Inactive-Upstream [foo]')
                             ],
                             )
    def test_inactive(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Inactive-Upstream'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'Inactive-Upstream [foo]'),
                                 _generate_input('diff', 'Inactive-Upstream [foo]')
                             ],
                             )
    def test_inactive_std(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.file.upstreamstatus_occurance.Inactive-Upstream'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 _generate_input('patch', 'SomethingElse'),
                                 _generate_input('diff', 'SomethingElse')
                             ],
                             )
    def test_inactive_no_hit(self, input_, id_, occurrence):
        _rule_file = self._create_tempfile('rules.json', json.dumps({id_: 'warning'}))
        self.check_for_id(self._create_args(input_, ['--rulefile=' + _rule_file]), id_, occurrence)
