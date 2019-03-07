try:
    from .cls_rule import Rule
except (SystemError, ImportError):
    from cls_rule import Rule

class NoSpaceRuleCont(Rule):
    def __init__(self):
        super().__init__(id = "oelint.spaces.linecont", 
                         severity="error",
                         message="No spaces after line continuation")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw:
                if i.Raw.find("\\ ") != -1:
                    res += self.finding(i.Origin, i.InFileLine)
        return res