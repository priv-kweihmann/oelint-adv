from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarSRCUriGitTag(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.srcuriappend',
                         severity='error',
                         message='<FOO>')

    def check(self, _file, stash):
        res = []
        inherits = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                     attribute=Variable.ATTR_VAR, attributeValue='inherit')
        if not inherits:
            return res

        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')
        for item in items:
            if any(item.Flag.endswith(x) for x in ['md5sum', 'sha256sum']):
                # These are just the hashes
                continue
            if item.VarOp.strip() in ['+=']:
                override_delimiter = item.OverrideDelimiter
                res += self.finding(item.Origin, item.InFileLine,
                                    'Use SRC_URI{od}append otherwise this will override weak defaults by inherit'.format(
                                        od=override_delimiter))
        return res
