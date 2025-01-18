from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class VarsRenamed(Rule):
    def __init__(self) -> None:
        self._map = CONSTANTS.GetByPath('variables/renamed')
        super().__init__(id='oelint.vars.renamed',
                         severity='error',
                         message='{var} {reason}',
                         valid_from_release='kirkstone')

    def __getMatches(self, _file: str, stash: Stash) -> List[Variable]:
        items: List[Variable] = stash.GetItemsFor(filename=_file,
                                                  classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR,
                                                  attributeValue=list(self._map.keys()))
        return items

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for i in self.__getMatches(_file, stash):
            message = self._map[i.VarName]
            if ' ' not in message:
                message = f'got renamed to {message}'
            res += self.finding(i.Origin, i.InFileLine,
                                self.Msg.format(var=i.VarName, reason=message))
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        for i in self.__getMatches(_file, stash):
            rename = self._map[i.VarName]
            if ' ' not in rename:
                stash.Remove(i)
                i.RealRaw = i.RealRaw.replace(i.VarName, rename)
                i.Raw = i.Raw.replace(i.VarName, rename)
                i = Variable(origin=i.Origin,
                             line=i.Line,
                             infileline=i.InFileLine,
                             rawtext=i.Raw,
                             realraw=rename,
                             inline_blocks=i.InlineBlocks,
                             new_style_override_syntax=i.IsNewStyleOverrideSyntax,
                             name=i.VarName,
                             value=i.VarValue,
                             operator=i.VarOp)
                stash.Append(i)
                res.append(_file)
        return res
