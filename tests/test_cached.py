import pytest  # noqa: I900
import os
import glob

from .base import TestBaseClass


# flake8: noqa S101 - n.a. for test files
class TestCached(TestBaseClass):

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'test.bb':
                                     '''
                                     INSANE_SKIP:${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_cached(self, capsys, input_):

        from oelint_adv.core import run
        from oelint_adv.__main__ import arguments_post

        tmpdir = os.path.dirname(self._create_tempfile('tmppath/.marker', ''))
        files = [self._create_tempfile(k, v) for k, v in input_.items()]

        args = arguments_post(self._create_args_parser().parse_args(
            ['--jobs=1', '--cached', f'--cachedir={tmpdir}', *files]
        ))

        run(args)

        captured = capsys.readouterr()

        assert 'Using cached item ' not in captured.out

        assert any(glob.glob(f'{tmpdir}/*'))

        run(args)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'test.bb':
                                     '''
                                     INSANE_SKIP:${PN} = "foo"
                                     ''',
                                 },
                             ],
                             )
    def test_no_cached(self, capsys, input_):

        from oelint_adv.core import run
        from oelint_adv.__main__ import arguments_post

        tmpdir = os.path.dirname(self._create_tempfile('tmppath/.marker', ''))
        files = [self._create_tempfile(k, v) for k, v in input_.items()]

        args = arguments_post(self._create_args_parser().parse_args(
            ['--jobs=1', *files]
        ))

        run(args)

        captured = capsys.readouterr()

        assert 'Using cached item ' not in captured.out

        assert not any(glob.glob(f'{tmpdir}/*'))

    def test_clear_cached(self):

        from oelint_adv.__main__ import arguments_post

        tmpdir = os.path.dirname(self._create_tempfile('tmppath/.marker', ''))

        args = arguments_post(self._create_args_parser().parse_args(
            ['--jobs=1', '--cached', f'--cachedir={tmpdir}', '--clear-caches']
        ))

        args.state._caches.ClearCaches()

    def test_arg_fingerprint(self):

        from oelint_adv.__main__ import arguments_post

        tmpdir = os.path.dirname(self._create_tempfile('tmppath/.marker', ''))

        args = arguments_post(self._create_args_parser().parse_args(
            ['--jobs=1', '--cached', f'--cachedir={tmpdir}', self._create_tempfile('test.bb', '')]
        ))

        fp = args.state._caches.FingerPrint

        args.state._caches.AddToFingerPrint(b'1234')

        assert args.state._caches.FingerPrint != fp

        args.state._caches.AddToFingerPrint('1234')

        assert args.state._caches.FingerPrint != fp
