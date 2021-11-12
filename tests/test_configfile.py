import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass  # noqa


class TestConfigFile(TestBaseClass):

    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_environ(self, input):
        # Test the default
        _args = self._create_args(input)

        assert not _args.nowarn

        # test the override from config file
        # here loaded via environment variable
        _cstfile = self._create_tempfile('oelint.cfg', '[oelint]\nnowarn=True')
        os.environ['OELINT_CONFIG'] = _cstfile
        _args = self._create_args(input)
        del os.environ['OELINT_CONFIG']
        
        assert _args.nowarn

    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_home(self, input):
        # Test the default
        _args = self._create_args(input)

        assert not _args.nowarn

        # test the override from config file
        # here loaded via home folder
        _cstfile = self._create_tempfile(
            '.oelint.cfg', '[oelint]\nnowarn=True')
        os.environ['HOME'] = os.path.dirname(_cstfile)
        _args = self._create_args(input)

        assert _args.nowarn

    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_workdir(self, input):
        # Test the default
        _args = self._create_args(input)

        assert not _args.nowarn

        # test the override from config file
        # here loaded from current workdir
        _cstfile = self._create_tempfile(
            '.oelint.cfg', '[oelint]\nnowarn=True')

        _cwd = os.getcwd()
        os.chdir(os.path.dirname(_cstfile))
        _args = self._create_args(input)
        os.chdir(_cwd)

        assert _args.nowarn

    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_boolean_options(self, input):
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
            _args = self._create_args(input)
            del os.environ['OELINT_CONFIG']

            assert isinstance(getattr(_args, _option), bool)

    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_no_convert(self, input):
        # Test if the following options remain untouched
        for _option in [
            'output',
            'addrules',
            'customrules',
            'messageformat',
        ]:
            _cstfile = self._create_tempfile(
                '.oelint.cfg', '[oelint]\n{item}=True'.format(item=_option))
            os.environ['OELINT_CONFIG'] = _cstfile
            _args = self._create_args(input)
            del os.environ['OELINT_CONFIG']

            assert getattr(_args, _option) == 'True'

    @pytest.mark.parametrize('input',
                             [
                                 {
                                     'oelint adv-test.bb': 'VAR = "1"',
                                 },
                             ],
                             )
    def test_config_file_multiple(self, input):
        # Test if the following options are converted to lists
        for _option in [
            'suppress'
        ]:
            _cstfile = self._create_tempfile(
                '.oelint.cfg', '[oelint]\n{item}=\t+True\n\t-False'.format(item=_option))
            os.environ['OELINT_CONFIG'] = _cstfile
            _args = self._create_args(input)

            assert isinstance(getattr(_args, _option), list)
            assert getattr(_args, _option) == ['+True', '-False']

    @pytest.mark.parametrize('input',
                        [
                            {
                                'oelint adv-test.bb': 'VAR = "1"',
                            },
                        ],
                        )
    def test_config_file_cli_always_wins(self, input):
        _cstfile = self._create_tempfile(
            '.oelint.cfg', '[oelint]\suppress=B')
        os.environ['OELINT_CONFIG'] = _cstfile
        _args = self._create_args(input, extraopts=['--suppress=A'])
        del os.environ['OELINT_CONFIG']

        assert getattr(_args, 'suppress') == ['A']

    @pytest.mark.parametrize('input',
                    [
                        {
                            'oelint adv-test.bb': 'VAR = "1"',
                        },
                    ],
                    )
    def test_config_file_messageformat(self, input):
        _cstfile = self._create_tempfile(
            '.oelint.cfg', '[oelint]\nmessageformat={severity}-{id}-{msg}')
        os.environ['OELINT_CONFIG'] = _cstfile
        _args = self._create_args(input)
        del os.environ['OELINT_CONFIG']

        assert getattr(_args, 'messageformat') == '{severity}-{id}-{msg}'

    @pytest.mark.parametrize('input',
                            [
                                {
                                    'oelint adv-test.bb': 'VAR = "1"',
                                },
                            ],
                            )
    def test_config_file_environ_broken(self, input):
        # Test the default
        _args = self._create_args(input)

        assert not _args.nowarn

        # test the override from config file
        # here loaded via environment variable but with a broken file
        _cstfile = self._create_tempfile('oelint.cfg', '[oel]\nnowarn=')
        os.environ['OELINT_CONFIG'] = _cstfile
        _args = self._create_args(input)
        del os.environ['OELINT_CONFIG']
        
        assert not _args.nowarn