import contextlib
import os

from .base import TestBaseClass

# flake8: noqa S101 - n.a. for test files


class TestColor(TestBaseClass):

    @contextlib.contextmanager
    def modified_env(**environ):
        _bak = dict(os.environ)
        os.environ.update(environ)
        try:
            yield
        finally:
            os.environ.clear()
            os.environ.update(_bak)

    def test_get_color_by_severity(self):
        # local scoped import required due PATH manipulation
        from oelint_adv import state
        assert isinstance(state.State().get_color_by_severity('info'), str)

    def test_get_color_by_severity_missing(self):
        # local scoped import required due PATH manipulation
        from oelint_adv import state
        assert state.State().get_color_by_severity('unknown') == ''

    def test_get_color_by_severity_no_color(self):
        # local scoped import required due PATH manipulation
        from oelint_adv import state
        with TestColor.modified_env(NO_COLOR='1'):
            assert isinstance(state.State().get_color_by_severity('info'), str)

    def test_get_color_by_severity_missing(self):
        # local scoped import required due PATH manipulation
        from oelint_adv import state
        with TestColor.modified_env(NO_COLOR='1'):
            assert state.State().get_color_by_severity('info') == ''
            assert state.State().get_color_by_severity('error') == ''
            assert state.State().get_color_by_severity('warning') == ''
            assert state.State().get_color_by_severity('unknown') == ''
