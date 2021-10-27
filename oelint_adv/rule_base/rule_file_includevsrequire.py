from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Include


class FileIncludeVsRequire(Rule):
    def __init__(self):
        super().__init__(id='oelint.file.requireinclude',
                         severity='warning',
                         message='Use \'require {FILE}\' instead of \'include {FILE}\'')

    def check(self, _file, stash):
        res = []
        for item in stash.GetItemsFor(filename=_file,
                                      classifier=Include.CLASSIFIER):
            if item.Statement == 'include':
                res += self.finding(item.Origin, item.Line,
                                    self.Msg.replace('{FILE}', item.IncName))
        return res
