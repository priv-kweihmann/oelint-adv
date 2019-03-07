try:
    from .cls_rule import Rule
except (SystemError, ImportError):
    from cls_rule import Rule

class NoTabs(Rule):
    def __init__(self):
        super().__init__(id = "oelint.tabs.notabs", 
                         severity="warning",
                         message="Don't use tabs use spaces")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw and "\t" in i.Raw:
                res += self.finding(i.Origin, i.InFileLine)
        return res