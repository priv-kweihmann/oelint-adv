import os
import re

from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarDependsOrdered(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.dependsordered',
                         severity='warning',
                         message='\'{VAR}\' entries should be ordered alphabetically')

    def __overrides(self, findings):
        res = {f.GetMachineEntry() for f in findings}
        res.update(f.GetClassOverride() for f in findings)
        return res

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        # ignore the settings from bbclasses
        items = [x for x in items if not x.Origin.endswith('.bbclass')]
        _keys = {x.VarName for x in items if re.match(
            r'DEPENDS|RDEPENDS', x.VarName)}
        _filegroups = {x.Origin for x in items}

        for _file in _filegroups:
            _, _ext = os.path.splitext(_file)
            if _ext not in ['.bb', '.bbappend']:
                continue
            for _key in _keys:
                _all_findings = sorted([x for x in items if (
                    x.Origin == _file or _file in x.IncludedFrom) and x.VarName == _key], key=lambda x: x.Line)
                for _m in sorted(self.__overrides(_all_findings), key=lambda x: len(x), reverse=True):
                    _raw_list = []
                    _machine_findings = sorted([x for x in _all_findings if _m == x.GetMachineEntry(
                    ) or _m == x.GetClassOverride()], key=lambda x: x.Line)
                    for item in _machine_findings:
                        _raw_list += item.get_items(versioned=True)
                        if _raw_list != sorted(_raw_list):
                            res += self.finding(item.Origin, item.InFileLine,
                                                override_msg=self.Msg.format(VAR=_key))
                            # quit on the first finding, as all following will be corrupted anyway
                            break
                    # Filter out every seen entry
                    _all_findings = [
                        x for x in _all_findings if x not in _machine_findings]
        return res
