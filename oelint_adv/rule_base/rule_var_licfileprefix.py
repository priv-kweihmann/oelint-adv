import os
from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarLicFilePrefix(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.licfileprefix',
                         severity='warning',
                         message='Prefix \'{PATH}\' to LIC_FILES_CHKSUM is not needed')

    def __getMatches(self, _file: str, stash: Stash) -> List[Variable]:
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='LIC_FILES_CHKSUM')
        for i in items:
            for listitem in i.get_items():
                _comp = stash.GetScrComponents(listitem)
                _prefix = os.path.dirname(_comp['src'])
                if _prefix in ['${S}']:
                    res.append(i)
        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for i in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, i.InFileLine,
                                override_msg=self.Msg.format(PATH='${S}'))
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        for i in self.__getMatches(_file, stash):
            i.RealRaw = i.RealRaw.replace('${S}/', '').replace('${S}', '')
            i.Raw = i.Raw.replace('${S}/', '').replace('${S}', '')
            res.append(_file)
        return res
