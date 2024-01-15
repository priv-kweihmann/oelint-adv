from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarLicenseRemoteFile(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.licenseremotefile',
                         severity='warning',
                         message='License-File should be a remote file')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                   attribute=Variable.ATTR_VAR, attributeValue='LIC_FILES_CHKSUM')
        _var_whitelist = ['${WORKDIR}', '${S}', '${B}']
        for i in _items:
            components = stash.GetScrComponents(stash.ExpandTerm(_file, i.VarValueStripped))
            if any(components) and components['scheme'] == 'file':
                _clean = components['src']
                for x in _var_whitelist:
                    _clean = _clean.replace(x, '')
                if '${' in _clean:
                    res += self.finding(i.Origin, i.InFileLine)
        return res
