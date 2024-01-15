from typing import List, Tuple

from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class NewLineEOF(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.newline.eof',
                         severity='warning',
                         message='File shall end on a newline')

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
            if not v[-1].Raw.endswith('\n'):
                res += self.finding(v[-1].Origin, v[-1].InFileLine)
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        for f, v in self.__getMatches(_file, stash).items():
            if not v[-1].RealRaw.endswith('\n'):
                v[-1].RealRaw += '\n'
                v[-1].Raw += '\n'
                res.append(f)
        return res
