from typing import List, Tuple

from oelint_parser.cls_item import Variable, Function
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import Constants

from oelint_adv.cls_rule import Rule, Classification


class VarSpecNonCore(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.noncoreoverride',
                         severity='error',
                         message="'{a}' need to be specific to a custom MACHINE or DISTRO to be Yocto project compliant",
                         run_on=[Classification.BBAPPEND])

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        self._core_constants = Constants(self._state.core_mod_ref)

        res = []
        items: List[Variable] = stash.GetItemsFor(
            filename=_file, classifier=(Variable.CLASSIFIER, Function.CLASSIFIER))
        for i in items:
            subs = [x for x in i.SubItems if x not in [
                'append', 'prepend', 'remove', '${PN}', '${BPN}']]
            if isinstance(i, Variable):
                name = i.VarName
                remaining_subs = [
                    x for x in subs if x not in self._core_constants.VariablesKnown]
            elif isinstance(i, Function):  # pragma: no cover
                name = i.FuncName
                remaining_subs = [
                    x for x in subs if x not in self._core_constants.FunctionsKnown]
            remaining_subs = [
                x for x in remaining_subs if x not in self._core_constants.DistrosKnown]
            remaining_subs = [
                x for x in remaining_subs if x not in self._core_constants.MachinesKnown]

            if not remaining_subs:
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(a=name))

        return res
