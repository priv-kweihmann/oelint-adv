from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class VarMultiLineIndent(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.multilineident',
                         severity='info',
                         message='On a multiline assignment, line indent is desirable. {a} set, {b} desirable')

    def __line_stats(self, raw: str) -> Tuple[int, List[str]]:
        _map = {}
        _lines = [x for x in RegexRpl.split(r'\t|\x1b', raw) if x and x.strip()]
        for index, value in enumerate(_lines):
            _map[index] = len(value) - len(value.lstrip())
        _distribution = {x: list(_map.values()).count(x)
                         for x in set(_map.values())}

        if not any(_distribution):
            return (0, list(_map.values()))

        return (max(_distribution, key=lambda x: _distribution[x]), list(_map.values()))

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if not i.IsMultiLine():
                continue
            _likeliest_indent, _indent_map = self.__line_stats(i.VarValueStripped)
            _likeliest_indent = max(4, _likeliest_indent)
            for index, value in enumerate(_indent_map):
                if value != _likeliest_indent:
                    res += self.finding(i.Origin, i.InFileLine + index,
                                        self.format_message(a=value, b=_likeliest_indent))
        return res
