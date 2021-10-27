from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable


class VarDependsSingleLine(Rule):
    def __init__(self):
        super().__init__(id='oelint.jetm.vars.dependssingleline',
                         severity='warning',
                         message='Each [R]DEPENDS entry should be put into a single line')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='DEPENDS')
        items += stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue='RDEPENDS')

        for i in items:
            if len(i.get_items(versioned=True)) > 1:
                res += self.finding(i.Origin, i.InFileLine)
        return res
