from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import *


class VarMultiLineIndent(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.multilineident",
                         severity="info",
                         message="On a multiline assignment, line indent is desirable. Current {}/{}")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if not i.IsMultiLine():
                continue
            _rawclean = i.GetRawCleaned()
            _needle = i.VarValue
            if len(_needle) > 10:
                _needle = _needle[:10]
            _value = _rawclean[_rawclean.find(_needle):]
            _lines = [x for x in _value.split("\\") if x]
            if any(_lines):
                _calcoffset = i.Raw.find(_lines[0])
                for _line in _lines[1:]:
                    _thisline = (len(_line) - len(_line.lstrip(" "))) - 1
                    if _thisline < _calcoffset:
                        res += self.finding(i.Origin, i.InFileLine + _lines.index(
                            _line), self.FormatMsg(_thisline, _calcoffset))
        return res
