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

    def __line_stats(self, raw: str, name: str, op: str) -> Tuple[int, List[str]]:
        _map = {}

        raw = raw.replace('\x1b"', '"')

        first_line_determines_indent = False
        # If the first line already has non-whitespace content, determine the alignment relative to the
        # first quotation mark.
        # Otherwise, try to guess the most common indentation from the other lines.
        if RegexRpl.match(r'^\s*\S\s*\x1b', raw):
            first_line_determines_indent = True

        _lines = [x for x in RegexRpl.split(r'\t|\x1b', raw) if x and x.strip()]
        for index, value in enumerate(_lines):
            if index == 0 and first_line_determines_indent:
                # the actual variable content starts after the name, the operator and the initial quotation mark
                _map[index] = len(name) + len(op) + 1
            else:
                _map[index] = len(value) - len(value.lstrip())
        _distribution = {x: list(_map.values()).count(x)
                         for x in set(_map.values())}

        if not any(_distribution):
            return (0, list(_map.values()))

        if first_line_determines_indent:
            return (_map[0], list(_map.values()))

        return (max(_distribution, key=lambda x: _distribution[x]), list(_map.values()))

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if not i.IsMultiLine():
                continue
            _likeliest_indent, _indent_map = self.__line_stats(i.VarValueStripped, i.VarNameComplete, i.VarOp)
            _likeliest_indent = max(4, _likeliest_indent)
            for index, value in enumerate(_indent_map):
                if value != _likeliest_indent:
                    res += self.finding(i.Origin, i.InFileLine + index,
                                        self.format_message(a=value, b=_likeliest_indent))
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if not i.IsMultiLine():
                continue
            _likeliest_indent, _indent_map = self.__line_stats(i.VarValueStripped, i.VarNameComplete, i.VarOp)
            _likeliest_indent = max(4, _likeliest_indent)
            _lines = i.RealRaw.splitlines()
            found = False
            for index, value in enumerate(_indent_map):
                if value != _likeliest_indent and index != 0:
                    found = True
                    _lines[index] = " " * _likeliest_indent + _lines[index].lstrip()
                    res.append(_file)
            if found:  # pragma: no cover
                i.Raw = "\n".join(_lines)
                i.RealRaw = "\n".join(_lines)
        return res
