from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class VarListAppend(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.listappend',
                         severity='error',
                         message='<FOO>')

    def __getMatches(self, _file: str, stash: Stash) -> Tuple[List[Variable], List[Variable]]:
        res_app = []
        res_pre = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR)

        for i in items:
            ops = i.AppendOperation()
            if RegexRpl.match('["|\'](\x1b)* ', i.VarValue) is None and any(x in ops for x in ['append', ' .= ']):
                res_app.append(i)
            if not i.VarValue.endswith(' "') and any(x in ops for x in ['prepend', ' =. ']) and ':=' not in i.VarOp:
                res_pre.append(i)
        return (res_app, res_pre)

    def check(self, _file: str, stash: Stash) -> List[Rule.Finding]:
        res = []
        res_app, res_pre = self.__getMatches(_file, stash)
        for i in res_app:
            res += self.finding(i.Origin, i.InFileLine,
                                override_msg='Append to list should start with a blank')
        for i in res_pre:
            res += self.finding(i.Origin, i.InFileLine,
                                override_msg='Prepend to list should end with a blank')
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        res_app, res_pre = self.__getMatches(_file, stash)
        for i in res_app:
            _m = RegexRpl.match('"(\x1b)*', i.VarValue)
            vv_rpl = i.VarValue.replace(_m.group(0), _m.group(0) + ' ', 1)
            i.RealRaw = i.RealRaw.replace(i.VarValue, vv_rpl)
            i.Raw = i.Raw.replace(i.VarValue, vv_rpl)
            i.VarValue = vv_rpl
            res.append(_file)
        for i in res_pre:
            _m = RegexRpl.match('["|\'](\x1b)*', i.VarValue[::-1])
            if _m is None:
                continue
            vv_rpl = i.VarValue[::-1].replace(_m.group(0), _m.group(0) + ' ', 1)[
                ::-1].replace('\x1b', '\\\n')
            vv_needle = i.VarValue.replace('\x1b', '\\\n')
            i.RealRaw = i.RealRaw.replace(vv_needle, vv_rpl)
            i.Raw = i.Raw.replace(vv_needle, vv_rpl)
            i.VarValue = vv_rpl
            res.append(_file)
        return res
