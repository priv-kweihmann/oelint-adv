from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarInconSpaces(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.inconspaces',
                         severity='error',
                         message='<FOO>')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            app_operation = i.AppendOperation()
            _stripped = i.VarValueStripped.lstrip(chr(0x1b))
            # allow 'spaceless' append to FILESEXTRAPATHS as there is
            # no operation which supports the combination of
            # append + :=
            if 'append' in app_operation and not _stripped.startswith(' ') and i.VarName in ['FILESEXTRAPATHS']:
                continue
            if ' += ' in app_operation and i.VarValueStripped.startswith(' '):
                res += self.finding(i.Origin, i.InFileLine,
                                    'Assignment should be \'VAR += "foo"\' not \'VAR += " foo"\'')
            if 'append' in app_operation and not _stripped.startswith(' '):
                override_delimiter = i.OverrideDelimiter
                res += self.finding(i.Origin, i.InFileLine,
                                    'Assignment should be \'VAR{od}append = " foo"\' not \'VAR{od}append = "foo"\''.format(
                                        od=override_delimiter))
        return res
