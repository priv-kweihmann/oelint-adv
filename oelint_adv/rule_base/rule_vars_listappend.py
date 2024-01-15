from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

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
                                                  attribute=Variable.ATTR_VAR,
                                                  attributeValue=['PACKAGES', 'SRC_URI', 'FILES', 'RDEPENDS', 'DEPENDS'])

        for i in items:
            ops = i.AppendOperation()
            if not i.VarValue.startswith('" ') and any(x in ops for x in ['append', ' .= ']):
                res_app.append(i)
            if not i.VarValue.endswith(' "') and any(x in ops for x in ['prepend', ' =. ']):
                res_pre.append(i)
        return (res_app, res_pre)

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
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
            vv_rpl = i.VarValue.replace('"', '" ', 1).replace('\'', '\' ', 1)
            i.RealRaw = i.RealRaw.replace(i.VarValue, vv_rpl)
            i.Raw = i.Raw.replace(i.VarValue, vv_rpl)
            i.VarValue = vv_rpl
            res.append(_file)
        for i in res_pre:
            vv_rpl = i.VarValue[::-1].replace('"', '" ', 1).replace('\'', '\' ', 1)[::-1]
            i.RealRaw = i.RealRaw.replace(i.VarValue, vv_rpl)
            i.Raw = i.Raw.replace(i.VarValue, vv_rpl)
            i.VarValue = vv_rpl
            res.append(_file)
        return res
