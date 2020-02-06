from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarSectionLowercase(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.sectionlowercase",
                         severity="warning",
                         message="'SECTION' should only lowercase characters")

    def __getMatches(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="SECTION")
        for i in items:
            if not i.VarValue.islower():
                res.append(i)
        return res

    def check(self, _file, stash):
        res = []
        for i in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, i.InFileLine)
        return res

    def fix(self, _file, stash):
        res = []
        for i in self.__getMatches(_file, stash):
            i.Raw = i.Raw.replace(i.VarValue, i.VarValue.lower())
            i.VarValue = i.VarValue.lower()
            res.append(_file)
        return res
