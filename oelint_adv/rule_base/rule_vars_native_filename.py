from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarNativeFilename(Rule):
    def __init__(self):
        super().__init__(id='oelint.var.nativefilename',
                         severity='warning',
                         message='native-recipe-files should include \'-native\' in file name')

    def check(self, _file, stash):
        res = []
        items = [x for x in
                 stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue='inherit')
                 if x.VarValueStripped == 'native']
        if any(items):
            if _file.find('-native') == -1:
                res += self.finding(_file, 0)
        return res
