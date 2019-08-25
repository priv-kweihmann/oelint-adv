from oelint_adv.cls_rule import Rule


class NoCommentsTrailing(Rule):
    def __init__(self):
        super().__init__(id="oelint.comments.notrailing",
                         severity="error",
                         message="Comments shall be put on seperate lines")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if i.Raw:
                for line in i.Raw.split("\n"):
                    line = line.strip()
                    if "#" in line and line.find("#") > 0:
                        res += self.finding(i.Origin, i.InFileLine)
        return res
