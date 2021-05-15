import os
import sys
import tempfile
import textwrap
import logging

import pytest


class TestBaseClass():

    TEST_UNDEFINED_PARAMETER = 'this is an undefined parameter to work around pytest limitations'

    @classmethod
    def setup_class(cls):
        sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))

    def __pytest_empty_object_fixture(self, _input, default):
        if _input == TestBaseClass.TEST_UNDEFINED_PARAMETER:
            return default
        return _input

    def _create_tempfile(self, _file, _input):
        self.__created_files = getattr(self, '__created_files', {})
        self._tmpdir = getattr(self, '_tmpdir', tempfile.mkdtemp())
        _path = os.path.join(self._tmpdir, _file)
        os.makedirs(os.path.dirname(_path), exist_ok=True)
        
        with open(_path, "w") as o:
            _cnt = textwrap.dedent(_input).lstrip("\n")
            self.__created_files[_file] = _cnt
            o.write(_cnt)
        return _path

    def _create_args(self, input, extraopts=[]):
        from oelint_adv.__main__ import arguments_post
        return arguments_post(self._create_args_parser().parse_args(
            ['--quiet'] + 
            self.__pytest_empty_object_fixture(extraopts, []) +
            [self._create_tempfile(k, v) for k, v in input.items()]
        ))

    def _create_args_fix(self, input, extraopts=[]):
        from oelint_adv.__main__ import arguments_post
        return arguments_post(self._create_args_parser().parse_args(
            ['--quiet', '--fix', '--nobackup'] + 
            self.__pytest_empty_object_fixture(extraopts, []) +
            [self._create_tempfile(k, v) for k, v in input.items()]
        ))

    def fix_and_check(self, args, id):
        from oelint_adv.__main__ import run
        # run for auto fixing
        run(args)
        # check run
        self.check_for_id(args, id, 0)

    def _create_args_parser(self):
        from oelint_adv.__main__ import create_argparser
        return create_argparser()

    def check_for_id(self, args, id, occurences):
        from oelint_adv.__main__ import run
        issues = [x[1] for x in run(args)]
        _files = '\n---\n'.join(['{}:\n{}'.format(k,v) for k,v in self.__created_files.items()])
        assert(len([x for x in issues if ':{}:'.format(id) in x]) ==
               occurences), '{} expected {} time(s) in:\n{}\n\n---\n{}'.format(id, occurences, '\n'.join(issues), _files)
