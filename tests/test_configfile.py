import os

import pytest  # noqa: I900

from .base import TestBaseClass
from oelint_adv.core import deserialize_boolean_options

# flake8: noqa S101 - n.a. for test files


class TestConfigFile(TestBaseClass):

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_environ(self, input_):
        # Test the default
        _args = self._create_args(input_)

        assert not _args.nowarn

        # test the override from config file
        # here loaded via environment variable
        _cstfile = self._create_tempfile('oelint.cfg', '[oelint]\nnowarn=True')
        os.environ['OELINT_CONFIG'] = _cstfile
        _args = self._create_args(input_)
        del os.environ['OELINT_CONFIG']

        assert _args.nowarn

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_home(self, input_):
        # Test the default
        _args = self._create_args(input_)

        assert not _args.nowarn

        # test the override from config file
        # here loaded via home folder
        _cstfile = self._create_tempfile(
            '.oelint.cfg', '[oelint]\nnowarn=True')
        os.environ['HOME'] = os.path.dirname(_cstfile)
        _args = self._create_args(input_)

        assert _args.nowarn

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_workdir(self, input_):
        # Test the default
        _args = self._create_args(input_)

        assert not _args.nowarn

        # test the override from config file
        # here loaded from current workdir
        _cstfile = self._create_tempfile(
            '.oelint.cfg', '[oelint]\nnowarn=True')

        _cwd = os.getcwd()
        os.chdir(os.path.dirname(_cstfile))
        _args = self._create_args(input_)
        os.chdir(_cwd)

        assert _args.nowarn

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_skip(self, input_):
        # Test the default
        _args = self._create_args(input_)

        assert not _args.nowarn

        # test the override from config file
        # here loaded from current workdir
        _cstfile = self._create_tempfile(
            '.oelint.cfg', '[oelint]\nnowarn=True')
        
        os.environ['OELINT_SKIP_CONFIG'] = '1'

        _cwd = os.getcwd()
        os.chdir(os.path.dirname(_cstfile))
        _args = self._create_args(input_)
        os.chdir(_cwd)

        os.environ.pop('OELINT_SKIP_CONFIG')

        assert not _args.nowarn

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_boolean_options(self, input_):
        # Test if the following options are auto converted
        # to boolean arguments
        for _option in [
            'color',
            'exit-zero',
            'fix',
            'nobackup',
            'noinfo',
            'nowarn',
            'print-rulefile',
            'quiet',
            'relpaths',
        ]:
            _cstfile = self._create_tempfile(
                '.oelint.cfg', '[oelint]\n{item}=True'.format(item=_option))
            os.environ['OELINT_CONFIG'] = _cstfile
            _args = self._create_args(input_)
            del os.environ['OELINT_CONFIG']

            assert isinstance(getattr(_args, _option.replace('-', '_')), bool)

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_no_convert(self, input_):
        # Test if the following options remain untouched
        for _option in [
            'output',
            'messageformat',
        ]:
            _cstfile = self._create_tempfile(
                '.oelint.cfg', '[oelint]\n{item}=True'.format(item=_option))
            os.environ['OELINT_CONFIG'] = _cstfile
            _args = self._create_args(input_)
            del os.environ['OELINT_CONFIG']

            assert getattr(_args, _option) == True

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_multiple(self, input_):
        # Test if the following options are converted to lists
        for _option in [
            'addrules',
            'customrules',
            'suppress',
        ]:
            _cstfile = self._create_tempfile(
                '.oelint.cfg', '[oelint]\n{item}=\t+True\n\t-False'.format(item=_option))
            os.environ['OELINT_CONFIG'] = _cstfile
            _args = self._create_args(input_)

            assert isinstance(getattr(_args, _option), list)
            assert getattr(_args, _option) == ['+True', '-False']

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_messageformat(self, input_):
        _cstfile = self._create_tempfile(
            '.oelint.cfg', '[oelint]\nmessageformat={severity}-{id}-{msg}')
        os.environ['OELINT_CONFIG'] = _cstfile
        _args = self._create_args(input_)
        del os.environ['OELINT_CONFIG']

        assert getattr(_args, 'messageformat') == '{severity}-{id}-{msg}'

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_environ_broken(self, input_):
        # Test the default
        _args = self._create_args(input_)

        assert not _args.nowarn

        # test the override from config file
        # here loaded via environment variable but with a broken file
        _cstfile = self._create_tempfile('oelint.cfg', '[oel]\nnowarn=')
        os.environ['OELINT_CONFIG'] = _cstfile
        _args = self._create_args(input_)
        del os.environ['OELINT_CONFIG']

        assert not _args.nowarn

    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_dash_replace(self, input_):
        # Test if the following options do the needed
        # - -> _ replacements automatically
        for _option in [
            'exit-zero',
            'print-rulefile',
        ]:
            _args = self._create_args(input_)
            assert not getattr(_args, _option.replace('-', '_'))

            _cstfile = self._create_tempfile(
                '.oelint.cfg', '[oelint]\n{item}=True'.format(item=_option))
            os.environ['OELINT_CONFIG'] = _cstfile
            _args = self._create_args(input_)
            del os.environ['OELINT_CONFIG']

            assert getattr(_args, _option.replace('-', '_'))


    def test_option_deserialization(self):
        options = {'a': 'True', 'b': True, 'c': 'False', 'd': False, 'e': 'other value'}
        deserialized = deserialize_boolean_options(options)
        assert deserialized == {'a': True, 'b': True, 'c': False, 'd': False, 'e': 'other value'}
