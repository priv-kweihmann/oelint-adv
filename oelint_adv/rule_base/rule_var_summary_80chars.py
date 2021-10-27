from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable


class VarSummary80Chars(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.summary80chars',
                         severity='warning',
                         message='\'SUMMARY\' should not be longer than 80 characters')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='SUMMARY')
        for i in items:
            val = i.VarValueStripped
            if len(val) > 80:
                res += self.finding(i.Origin, i.InFileLine)
        return res
