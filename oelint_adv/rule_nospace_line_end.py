try:
    from .cls_rule import Rule
except (SystemError, ImportError):
    from cls_rule import Rule

class NoSpaceTrailingRule(Rule):
    def __init__(self):
        super().__init__(id = "oelint.spaces.lineend", 
                         severity="warning",
                         message="Line shall not end with a space")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            _linecnt = 0
            for line in i.Raw.split("\n"):
                if line.endswith(" "):
                    res += self.finding(i.Origin, i.InFileLine + _linecnt)
                _linecnt += 1
        return res