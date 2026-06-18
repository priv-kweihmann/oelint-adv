from .base import TestBaseClass

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
