try:
    from .cls_rule import Rule
except (SystemError, ImportError):
    from cls_rule import Rule

class NoSpaceBeginningRule(Rule):
    def __init__(self):
        super().__init__(id = "oelint.spaces.linebeginning", 
                         severity="warning",
                         message="Line shall not begin with a space")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw and i.Raw.startswith(" "):
                res += self.finding(i.Origin, i.InFileLine)
        return res