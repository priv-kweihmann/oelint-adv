from typing import List, Tuple

from oelint_parser.cls_item import Function
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarDUsageInPkgfunc(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.dusageinpkgfuncs',
                         severity='error',
                         message='Use $D instead of ${{D}} in {func}')

    def __getMatches(self, _file: str, stash: Stash) -> List[Function]:
        res = []
        items: List[Function] = stash.GetItemsFor(filename=_file,
                                                  classifier=Function.CLASSIFIER,
                                                  attribute=Function.ATTR_FUNCNAME,
                                                  attributeValue=[
                                                      'pkg_preinst',
                                                      'pkg_postinst',
                                                      'pkg_postrm',
                                                      'pkg_prerm',
                                                  ],
                                                  )
        for i in items:
            if '${D}' in i.FuncBodyRaw:
                res.append(i)
        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for i in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format(func=i.FuncName))
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        for i in self.__getMatches(_file, stash):
            i.RealRaw = i.RealRaw.replace('${D}', '$D')
            i.Raw = i.Raw.replace('${D}', '$D')
            res.append(_file)
        return res
