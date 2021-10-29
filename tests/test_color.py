import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass  # noqa


class TestColor(TestBaseClass):

    def test_get_color_by_severity(self):
        from oelint_adv import color  # local scoped import required due PATH manipulation
        assert isinstance(color.get_color_by_severity("info"), str)

    def test_get_color_by_severity_missing(self):
        from oelint_adv import color  # local scoped import required due PATH manipulation
        assert color.get_color_by_severity("unknown") == ""
