import os
import shutil
import tempfile
import textwrap


# flake8: noqa S101 - n.a. for test files
class TestBaseClass:

    TEST_UNDEFINED_PARAMETER = 'this is an undefined parameter to work around pytest limitations'

    def __pytest_empty_object_fixture(self, _input, default):
        if _input == TestBaseClass.TEST_UNDEFINED_PARAMETER:
            return default
        return _input

    def _create_tempfile(self, _file, _input):
        self.__created_files = getattr(self, '__created_files', {})
        self._collected_tmpdirs = getattr(self, '_collect_tmpdirs', [])
        self._tmpdir = getattr(self, '_tmpdir', tempfile.mkdtemp())
        self._collected_tmpdirs.append(self._tmpdir)
        _path = os.path.join(self._tmpdir, _file)
        os.makedirs(os.path.dirname(_path), exist_ok=True)

        with open(_path, 'w') as o:
            _cnt = textwrap.dedent(_input).lstrip('\n')
            self.__created_files[_file] = _cnt
            o.write(_cnt)
        return _path

    def _create_args(self, input_, extraopts=None):
        if extraopts is None:
            extraopts = []
        from oelint_adv.__main__ import arguments_post
        return arguments_post(self._create_args_parser().parse_args(
            # noqa: W504 - we need to concat lists here
            ['--quiet', '--jobs=1'] +
            # noqa: W504 - we need to concat lists here
            self.__pytest_empty_object_fixture(extraopts, []) +
            [self._create_tempfile(k, v) for k, v in input_.items()],
        ))

    def _create_args_fix(self, input_, extraopts=None):
        if extraopts is None:
            extraopts = []
        from oelint_adv.__main__ import arguments_post
        return arguments_post(self._create_args_parser().parse_args(
            # noqa: W504 - we need to concat lists here
            ['--quiet', '--fix', '--nobackup', '--jobs=1'] +
            # noqa: W504 - we need to concat lists here
            self.__pytest_empty_object_fixture(extraopts, []) +
            [self._create_tempfile(k, v) for k, v in input_.items()],
        ))

    def fix_and_check(self, args, id_):
        from oelint_adv.__main__ import run
        # run for auto fixing
        run(args)

        args.fix = False

        # check run
        self.check_for_id(args, id_, 0)

    def _create_args_parser(self):
        from oelint_adv.__main__ import create_argparser
        return create_argparser()

    def check_for_id(self, args, id_, occurrences):
        from oelint_adv.__main__ import run
        issues = [x[1] for x in run(args)]
        _files = '\n---\n'.join(['{k}:\n{v}'.format(k=k, v=v)
                                 for k, v in self.__created_files.items()])
        assert(len([x for x in issues if ':{id}:'.format(id=id_) in x]) ==
               occurrences), '{id} expected {o} time(s) in:\n{i}\n\n---\n{f}'.format(id=id_, o=occurrences, i='\n'.join(issues), f=_files)

    def teardown(self):
        if getattr(self, '_collected_tmpdirs', None) is not None:
            for x in self._collected_tmpdirs:
                shutil.rmtree(x, ignore_errors=True)