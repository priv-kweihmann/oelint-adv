from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


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
            _rawclean = i.Raw
            _startoffset = _rawclean.find("= \"") + 3
            _value = _rawclean[_startoffset:]
            _lines = [x for x in _value.split("\\\n") if x]
            if any(_lines):
                for _line in _lines[1:]:
                    _linestripped = _line.lstrip('"').strip().lstrip('"').strip()
                    _thisline = (len(_line) - len(_line.lstrip(" ")))
                    if _thisline < 0 or not _linestripped:
                        continue
                    if _thisline < _startoffset:
                        res += self.finding(i.Origin, i.InFileLine + _lines.index(
                            _line), self.FormatMsg(_thisline, _startoffset))
        return res
