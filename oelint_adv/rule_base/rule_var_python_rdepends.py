from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule, Classification


class VarPythonRdepends(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.pythonrdepends',
                         severity='warning',
                         run_on=[Classification.BBAPPEND,
                                 Classification.RECIPE],
                         message='{var} installs the entire python ecosystem. Most likely you only want sub packages like {var}-core',
                         valid_from_release='scarthgap')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file,
                                                  classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR,
                                                  attributeValue='RDEPENDS')
        for item in items:
            for needle in ['python', 'python3', '${PYTHON_PN}']:
                if needle in item.get_items():
                    res += self.finding(item.Origin, item.InFileLine,
                                        self.Msg.format(var=needle))
        return res
