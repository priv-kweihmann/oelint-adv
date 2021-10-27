from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Function


class TaskMultiFragments(Rule):
    def __init__(self):
        super().__init__(id='oelint.task.multifragments',
                         severity='info',
                         message='Multiple fragments of the same function in the same file should be merged')

    def check(self, _file, stash):
        res = []
        _stash = stash.GetItemsFor(
            filename=_file, classifier=Function.CLASSIFIER)
        _known_matches = []
        for item in _stash:
            _needle = (item.FuncName, item.SubItem, item.Origin)
            if _needle in _known_matches:
                res += self.finding(item.Origin, item.InFileLine)
            _known_matches.append(_needle)
        return res
