from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import PythonBlock, Function


class NoCommentsTrailing(Rule):
    def __init__(self):
        super().__init__(id="oelint.comments.notrailing",
                         severity="error",
                         message="Comments shall be put on seperate lines")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if isinstance(i, PythonBlock) or isinstance(i, Function):
                continue
            if i.Raw:
                lines = i.Raw.split("\n")
                for line in lines:
                    _line = line.strip()
                    if "#" in _line and _line.find("#") > 0:
                        res += self.finding(i.Origin, i.InFileLine + lines.index(line))
        return res
