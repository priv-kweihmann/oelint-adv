from typing import List, Tuple

from oelint_parser.cls_item import FunctionExports, Inherit, Item, Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Classification, Rule


class VarOutOfContext(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.outofcontext',
                         severity='warning',
                         message='{var} should be only set in {context}')

    def _check(self,
               results: List[Tuple[str, int, str]],
               items: List[Item],
               valid_context: List[Classification],
               var_desc: str,
               context_desc: str = '') -> None:
        for item in items:
            classification = Rule.classify_file(item.Origin) or [Classification.RECIPE]
            if not any(set(classification).intersection(valid_context)):
                context = context_desc or ",".join(f'{Classification.tostr(x)}(s)' for x in valid_context)
                results += self.finding(item.Origin, item.InFileLine,
                                        override_msg=self.Msg.format(var=var_desc, context=context))

    def _is_image(self, _file: str, stash: Stash):
        res = False
        _inherits = stash.GetItemsFor(filename=_file, classifier=Inherit.CLASSIFIER)
        for item in _inherits:
            res |= any(True for x in item.get_items() if x in CONSTANTS.ImagesClasses)
        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []

        for var in CONSTANTS.GetByPath('oelint-contextvars/conf-only'):
            self._check(res, stash.GetItemsFor(filename=_file,
                                               classifier=Variable.CLASSIFIER,
                                               attribute=Variable.ATTR_VAR,
                                               attributeValue=var),
                        [Classification.LAYERCONF, Classification.MACHINECONF, Classification.DISTROCONF],
                        var_desc=var)
        for var in CONSTANTS.GetByPath('oelint-contextvars/bbappend-only'):
            self._check(res, stash.GetItemsFor(filename=_file,
                                               classifier=Variable.CLASSIFIER,
                                               attribute=Variable.ATTR_VAR,
                                               attributeValue=var),
                        [Classification.BBAPPEND],
                        var_desc=var)

        for var in CONSTANTS.GetByPath('oelint-contextvars/bbclass-only'):
            self._check(res, stash.GetItemsFor(filename=_file,  # pragma: no cover
                                               classifier=Variable.CLASSIFIER,
                                               attribute=Variable.ATTR_VAR,
                                               attributeValue=var),
                        [Classification.BBCLASS],
                        var_desc=var)

        for var in CONSTANTS.GetByPath('oelint-contextvars/recipe-only'):
            self._check(res, stash.GetItemsFor(filename=_file,
                                               classifier=Variable.CLASSIFIER,
                                               attribute=Variable.ATTR_VAR,
                                               attributeValue=var),
                        [Classification.BBCLASS, Classification.BBAPPEND, Classification.RECIPE],
                        var_desc=var)
        for var in CONSTANTS.GetByPath('oelint-contextvars/image-only'):
            if self._is_image(_file, stash):
                continue
            self._check(res, stash.GetItemsFor(filename=_file,
                                               classifier=Variable.CLASSIFIER,
                                               attribute=Variable.ATTR_VAR,
                                               attributeValue=var),
                        [Classification.MACHINECONF, Classification.DISTROCONF],
                        var_desc=var,
                        context_desc='file(s) that define image(s)')

        self._check(res, stash.GetItemsFor(filename=_file,
                                           classifier=FunctionExports.CLASSIFIER),
                    [Classification.BBCLASS],
                    var_desc='EXPORT_FUNCTIONS')

        self._check(res, stash.GetItemsFor(filename=_file,
                                           classifier=Inherit.CLASSIFIER,
                                           attribute=Inherit.ATTR_CLASS,
                                           attributeValue=['native', 'nativesdk', 'cross']),
                    [Classification.BBCLASS, Classification.BBAPPEND, Classification.RECIPE],
                    var_desc='inherit native, nativesdk, cross')

        return res
