from typing import List, Tuple

from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class NewLineConsecutive(Rule):
    def __init__(self):
        super().__init__(id='oelint.newline.consecutive',
                         severity='warning',
                         message='Consecutive blank lines should be avoided')

    def __getMatches(self, _file: str, stash: Stash) -> dict:
        res = {}
        items = stash.GetItemsFor(filename=_file)
        for _uniqname in {x.Origin for x in items}:
            res[_uniqname] = sorted(stash.GetItemsFor(
                filename=_uniqname, nolink=True), key=lambda x: x.InFileLine)
        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for _, v in self.__getMatches(_file, stash).items():
            for index, value in enumerate(v):
                if index == 0:
                    continue
                if value.Raw == '\n' and v[index - 1].Raw == '\n':
                    res += self.finding(value.Origin, value.InFileLine)
        return res
