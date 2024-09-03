from typing import List, Tuple

from oelint_parser.cls_item import Inherit
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarInheritLast(Rule):
    def __init__(self) -> None:
        self._needles = [
            'cross',
            'native',
            'nativesdk',
        ]
        super().__init__(id='oelint.var.inheritlast',
                         severity='warning',
                         message='{VAR} needs to be inherited last',
                         appendix=self._needles)

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Inherit] = stash.GetItemsFor(filename=_file, classifier=Inherit.CLASSIFIER)
        _findings = []
        for i in items:
            for class_ in i.get_items():
                _findings.append((class_, i))

        _findings_class_only = [x[0] for x in _findings]
        for needle in self._needles:
            if needle in _findings_class_only and _findings[-1][0] != needle:
                try:
                    index = next(i for i, v in enumerate(_findings) if v[0] == needle)  # pragma: no cover
                    res += self.finding(_findings[index][1].Origin, _findings[index][1].InFileLine,
                                        self.Msg.format(VAR=needle),
                                        appendix=needle)
                except StopIteration:  # pragma: no cover
                    continue  # pragma: no cover
        return res
