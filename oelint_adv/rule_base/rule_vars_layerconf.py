import fnmatch
from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule, Classification


class VarsLayerConf(Rule):
    def __init__(self) -> None:
        self.good = [
            r'BBFILES',
            r'BBFILES_DYNAMIC',
            r'BBFILE_COLLECTIONS',
            r'BBFILE_PATTERN_.*',
            r'BBFILE_PRIORITY_.*',
            r'BBPATH',
            r'HOSTTOOLS_NONFATAL',
            r'LAYERDEPENDS_.*',
            r'LAYERRECOMMENDS_.*',
            r'LAYERSERIES_COMPAT_.*',
            r'LAYERVERSION_.*',
            r'LICENSE_PATH',
        ]

        super().__init__(id='oelint.vars.layerconf',
                         severity='warning',
                         run_on=[Classification.LAYERCONF],
                         message='{var} should not be set as part of a layer configuration')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR)

        for i in items:
            if not fnmatch.fnmatch(i.Origin, '*/layer.conf'):
                continue
            if not any(RegexRpl.match(x, i.VarName) for x in self.good):
                res += self.finding(_file, i.InFileLine,
                                    self.Msg.format(var=i.VarName))
        return res
