from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Function
from oelint_parser.rpl_regex import RegexRpl


class TaskInstallNoCp(Rule):
    def __init__(self):
        super().__init__(id='oelint.task.heredocs',
                         severity='warning',
                         message='Usage of heredocs should be avoided. Use files instead')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER,
                                  attribute=Function.ATTR_FUNCNAME)
        for i in items:
            for index, line in enumerate(i.get_items()):
                line = line.strip()
                if RegexRpl.match(r'^cat\s*>\s*.*<<\s*[A-Za-z0-9]+$', line) or RegexRpl.match(r'^cat\s*<<\s*[A-Za-z0-9]+\s*>.*$', line):
                    res += self.finding(i.Origin, i.InFileLine + index)
        return res
