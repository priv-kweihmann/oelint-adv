from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Include
from oelint_parser.cls_item import Variable


class VarDependsAppend(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.dependsappend',
                         severity='error',
                         message='DEPENDS should only be appended, not overwritten as an include or inherit')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='DEPENDS')
        incinh = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='inherit', nolink=True)
        incinh += stash.GetItemsFor(filename=_file, classifier=Include.CLASSIFIER, nolink=True)

        earliest = 99999999
        if incinh:
            earliest = min(x.Line for x in incinh)

        for i in items:
            if not i.AppendOperation() and i.Line > earliest:
                res += self.finding(i.Origin, i.InFileLine)
        return res
