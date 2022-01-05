from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable


class VarBbclassextend(Rule):
    def __init__(self):
        super().__init__(id='oelint.var.bbclassextend',
                         severity='info',
                         message='BBCLASSEXTEND should be set if possible')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='BBCLASSEXTEND')
        items_inherit = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue='inherit')
        if not any(items):
            _safe = False
            for _class in ['native', 'nativesdk', 'cross']:
                if any([x for x in items_inherit if x.VarValue.find(_class) != -1]):
                    _safe = True
                    break
            if not _file.endswith('.bbappend') and not _safe:
                res += self.finding(_file, 0)
        return res
