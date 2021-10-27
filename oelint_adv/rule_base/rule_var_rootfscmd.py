from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable


class VarRootfsPostprocessCommand(Rule):
    def __init__(self):
        super().__init__(id='oelint.var.rootfspostcmd',
                         severity='warning',
                         message='ROOTFS_POSTPROCESS_COMMAND should not have trailing blanks')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        for i in [x for x in items if x.VarName.startswith('ROOTFS_POSTPROCESS_COMMAND')]:
            _chunks = i.VarValueStripped.split(';')
            if any(True for x in _chunks if x.strip() and x.endswith(' ')):
                res += self.finding(i.Origin, i.InFileLine)
        return res
