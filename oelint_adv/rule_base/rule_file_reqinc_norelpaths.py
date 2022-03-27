from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Include
from oelint_parser.helper_files import expand_term


class FileReqIncNoRelPaths(Rule):
    def __init__(self):
        super().__init__(id='oelint.file.includerelpath',
                         severity='warning',
                         message='include or require statements should not use relative paths. Try using bbclasses instead')

    def check(self, _file, stash):
        res = []
        for item in stash.GetItemsFor(filename=_file,
                                      classifier=Include.CLASSIFIER):
            _path = expand_term(stash, _file, item.IncName)
            if '..' in _path.split('/'):
                res += self.finding(item.Origin, item.InFileLine)
        return res
