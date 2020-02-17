from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarInconSpaces(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.inconspaces",
                         severity="error",
                         message="<FOO>")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            app_operation = i.AppendOperation()
            if " += " in app_operation and i.VarValueStripped.startswith(" "):
                res += self.finding(i.Origin, i.InFileLine,
                                    "Assignment should be 'VAR += \"foo\"' not 'VAR += \" foo\"'")
            if "append" in app_operation and not i.VarValueStripped.startswith(" "):
                res += self.finding(i.Origin, i.InFileLine,
                                    "Assignment should be 'VAR_append = \" foo\"' not 'VAR_append = \"foo\"'")
        return res
