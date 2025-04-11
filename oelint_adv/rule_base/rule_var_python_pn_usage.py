from typing import List, Tuple

from oelint_parser.cls_item import Function, Item, PythonBlock, Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule, Classification


class VarPythonPnUsage(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.pythonpnusage',
                         severity='info',
                         run_on=[Classification.BBAPPEND, Classification.RECIPE],
                         message='python3 should be used instead of ${PYTHON_PN}',
                         valid_from_release='scarthgap')

    def __getMatches(self, _file: str, stash: Stash) -> List[Tuple[Item, List[str]]]:
        res = []
        items: List[Item] = stash.GetItemsFor(filename=_file,
                                              classifier=[
                                                  Variable.CLASSIFIER,
                                                  Function.CLASSIFIER,
                                                  PythonBlock.CLASSIFIER,
                                              ])
        for i in items:
            if i.Origin.endswith('.bbclass'):
                continue
            if isinstance(i, PythonBlock):
                needles = ['${PYTHON_PN}', 'd.getVar("PYTHON_PN")', 'd.getVar(\'PYTHON_PN\')']
            elif isinstance(i, (Function, Variable)):
                needles = ['${PYTHON_PN}']
            else:
                needles = []  # pragma: no cover
            if any(x in i.Raw for x in needles):
                res.append((i, needles))
        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for i in self.__getMatches(_file, stash):
            item, _ = i
            res += self.finding(item.Origin, item.InFileLine)
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        for i in self.__getMatches(_file, stash):
            item, needles = i
            for needle in needles:
                item.RealRaw = item.RealRaw.replace(needle, 'python3')
                item.Raw = item.Raw.replace(needle, 'python3')
            res.append(_file)
        return res
