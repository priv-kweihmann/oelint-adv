from oelint_adv.cls_item import MissingFile
from oelint_adv.cls_rule import Rule


class FileRequireNotFound(Rule):
    def __init__(self):
        super().__init__(id="oelint.file.requirenotfound",
                         severity="error",
                         message="'{FILE}' was not found")

    def check(self, _file, stash):
        res = []
        for item in stash.GetItemsFor(filename=_file,
                                      classifier=MissingFile.CLASSIFIER):
            if item.Statement == "require":
                res += self.finding(item.Origin, item.InFileLine, self.Msg.replace("{FILE}", item.Filename))
        return res
