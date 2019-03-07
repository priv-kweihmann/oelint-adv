try:
    from .cls_rule import Rule
except (SystemError, ImportError):
    from cls_rule import Rule

class NoSpaceEmptyLineRule(Rule):
    def __init__(self):
        super().__init__(id = "oelint.spaces.emptyline", 
                         severity="warning",
                         message="Empty lines shall not contain spaces")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw.strip("\n") and not i.Raw.strip():
                res += self.finding(i.Origin, i.InFileLine)
        return res