from typing import List, Tuple

from oelint_parser.cls_item import Function
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class TaskInstallNoCp(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.task.nocopy',
                         severity='error',
                         message='\'cp\' shall not be used in do_install. Use \'install\'')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Function] = stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER)
        for item in items:
            if item.FuncName.startswith('do_install'):
                for lineindex, line in enumerate(item.get_items()):
                    if line.strip().startswith('#'):
                        continue
                    if (RegexRpl.search(r'^\s*cp ', line) or RegexRpl.search(r'\s+cp ', line)) and not RegexRpl.search(
                            r'\s*cp\s+(-R|-r)', line):
                        res += self.finding(item.Origin,
                                            item.InFileLine + lineindex, blockoffset=item.InFileLine)
        return res
