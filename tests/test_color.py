from .base import TestBaseClass

# flake8: noqa S101 - n.a. for test files
class TestColor(TestBaseClass):

    def test_get_color_by_severity(self):
        # local scoped import required due PATH manipulation
        from oelint_adv import color
        assert isinstance(color.get_color_by_severity('info'), str)

    def test_get_color_by_severity_missing(self):
        # local scoped import required due PATH manipulation
        from oelint_adv import color
        assert color.get_color_by_severity('unknown') == ''
