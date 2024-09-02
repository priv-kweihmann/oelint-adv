import tempfile

from .base import TestBaseClass


# flake8: noqa S101 - n.a. for test files
class TestLibMode(TestBaseClass):

    def test_libmode(self):
        test_recipe = '''
        INSANE_SKIP:${PN} = "foo"
        '''

        tmp_file = self._create_tempfile('test.bb', test_recipe)

        from oelint_adv.core import create_lib_arguments, run

        results = run(create_lib_arguments([tmp_file]))

        assert isinstance(results, list)
        assert len(results) > 0

        issues = [x[1] for x in results]

        assert len([x for x in issues if ':{id}:'.format(id='oelint.vars.insaneskip') in x]) == 1
