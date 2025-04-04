import os
from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule, Classification


class FilePatchIsSignedOff(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.file.patchsignedoff',
                         severity='warning',
                         run_on=[Classification.BBAPPEND, Classification.RECIPE],
                         message='Patch \'{FILE}\' should contain a Signed-off-by entry')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items = stash.GetFiles(_file, '*.patch')
        _items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                   attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')
        for i in items:
            with open(i) as _input:
                try:
                    content = _input.readlines()
                    if not any(x for x in content if x.startswith('Signed-off-by: ')):
                        # Find matching SRC_URI assignment
                        _assign = [x for x in _items if x.VarValue.find(
                            os.path.basename(i)) != -1]
                        if any(_assign):  # pragma: no cover
                            res += self.finding(_assign[0].Origin,
                                                _assign[0].InFileLine,
                                                self.Msg.replace('{FILE}', os.path.basename(i)))
                except UnicodeDecodeError:  # pragma: no cover
                    pass  # pragma: no cover
        return res
