import pytest  # noqa: I900

from .base import TestBaseClass

import hashlib
import json

# flake8: noqa S101 - n.a. for test files


class TestOutputFormat(TestBaseClass):

    def test_output_stderr_console(self, capsys):
        from oelint_adv.__main__ import run
        from oelint_adv.outputformat import _OUTPUT_FORMATS
        _args = self._create_args({'test.bb': 'A="1"'})
        _issues, _ = run(_args)
        capsys.readouterr()
        _OUTPUT_FORMATS[_args.outputformat](_args, _issues)
        captured = capsys.readouterr()
        assert ":oelint.vars.spacesassignment:Suggest spaces around" in captured.err
        assert not captured.out

    def test_output_junit_bad(self, capsys):
        from oelint_adv.__main__ import run
        from oelint_adv.outputformat import _OUTPUT_FORMATS
        _args = self._create_args({'test.bb': 'A="1"'}, [
                                  '--outputformat=junit'])
        _issues, _ = run(_args)
        capsys.readouterr()
        _OUTPUT_FORMATS[_args.outputformat](_args, _issues)
        captured = capsys.readouterr()
        assert '<?xml version="1.0" encoding="UTF-8"?>' in captured.err
        assert '<testsuite id="oelint-adv" name="oelint-adv"' in captured.err
        assert '<testcase name="oelint.vars.spacesassignment"' in captured.err
        assert '<failure message="oelint.vars.spacesassignment" type="failure">' in captured.err
        assert not captured.out

    def test_output_junit_good(self, capsys):
        from oelint_adv.__main__ import run
        from oelint_adv.outputformat import _OUTPUT_FORMATS
        _args = self._create_args({'test.bbappend': 'A = "1"\n'}, [
                                  '--outputformat=junit',
                                  '--suppress=oelint.vars.mispell',
                                  '--suppress=oelint.vars.noncoreoverride'])
        _issues, _ = run(_args)
        capsys.readouterr()
        _OUTPUT_FORMATS[_args.outputformat](_args, _issues)
        captured = capsys.readouterr()
        assert '<?xml version="1.0" encoding="UTF-8"?>' in captured.err
        assert '<testsuite id="oelint-adv" name="oelint-adv" tests="1" failures="0" errors="0" skipped="0">' in captured.err
        assert '<testcase name="oelint.run.passed"/>' in captured.err
        assert not captured.out

    def test_output_gitlab_bad(self, capsys):
        from oelint_adv.__main__ import run
        from oelint_adv.outputformat import _OUTPUT_FORMATS

        _args = self._create_args({'test.bb': 'A="1"'}, [
                                  '--outputformat=gitlab-codequality'])
        _issues, _ = run(_args)
        capsys.readouterr()
        _OUTPUT_FORMATS[_args.outputformat](_args, _issues)
        captured = capsys.readouterr()

        j = json.loads(captured.err)
        assert isinstance(j, list)
        [spacesassignment] = [x for x in j if x['check_name']
                              == 'oelint.vars.spacesassignment']
        assert spacesassignment is not None
        self._verify_json_finding(spacesassignment,
                                  check_name='oelint.vars.spacesassignment',
                                  file='test.bb',
                                  line=1,
                                  severity_oelint='warning',
                                  severity_gitlab='minor',
                                  text='Suggest spaces around assignment')

        assert not captured.out

    @pytest.mark.parametrize('severity',
                             [
                                 ('info', 'info'),
                                 ('warning', 'minor'),
                                 ('error', 'critical')
                             ],
                             )
    def test_output_gitlab_severity_conversion(self, capsys, severity):
        from oelint_adv.__main__ import run
        from oelint_adv.outputformat import OutputFormatGitlabCodequality

        _args = self._create_args({'test.bb': 'A="1"'}, [])

        _issues = [[["unused", 1, "unused", severity[0]], "unused"]]
        OutputFormatGitlabCodequality(_args, _issues)
        captured = capsys.readouterr()
        j = json.loads(captured.err)
        assert j[0]['severity'] == severity[1]

        assert isinstance(j, list)

    def test_output_gitlab_good(self, capsys):
        from oelint_adv.__main__ import run
        from oelint_adv.outputformat import _OUTPUT_FORMATS
        _args = self._create_args({'test.bbappend': 'A = "1"\n'}, [
                                  '--outputformat=gitlab-codequality',
                                  '--suppress=oelint.vars.mispell',
                                  '--suppress=oelint.vars.noncoreoverride'])
        _issues, _ = run(_args)
        capsys.readouterr()
        _OUTPUT_FORMATS[_args.outputformat](_args, _issues)
        captured = capsys.readouterr()
        assert captured.err == "[]"
        assert not captured.out

    def _verify_json_finding(self, j: dict,
                             check_name: str,
                             file: str, line: int,
                             severity_oelint: str, severity_gitlab: str,
                             text: str):
        assert j['check_name'] == check_name
        assert j['severity'] == severity_gitlab
        desc = j['description'].split(':', maxsplit=4)
        assert desc[2] == severity_oelint
        assert text in desc[4]
        assert j['fingerprint'] == hashlib.sha256(j['description'].encode('utf-8')).hexdigest()
        assert j['location']['path'].endswith(file)
        assert line == j['location']['lines']['begin']
