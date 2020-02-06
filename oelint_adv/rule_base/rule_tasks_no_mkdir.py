from oelint_adv.cls_item import Function
from oelint_adv.cls_rule import Rule


class TaskInstallNoMkdir(Rule):
    def __init__(self):
        super().__init__(id="oelint.task.nomkdir",
                         severity="error",
                         message="'mkdir' shall not be used in do_install. Use 'install'")

    def check(self, _file, stash):
        res = []
        for item in stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER):
            if item.FuncName.startswith("do_install"):
                if item.FuncBody.find(" mkdir ") != -1:
                    res += self.finding(item.Origin, item.InFileLine)
        return res
