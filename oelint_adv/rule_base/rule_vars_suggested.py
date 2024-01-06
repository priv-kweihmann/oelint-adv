from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.constants import CONSTANTS
from oelint_parser.helper_files import is_packagegroup


class VarSuggestedExists(Rule):
    def __init__(self):
        super().__init__(id='oelint.var.suggestedvar',
                         severity='info',
                         message='<FOO>',
                         onappend=False,
                         appendix=CONSTANTS.VariablesSuggested)

    def check(self, _file, stash):
        res = []
        _is_pkg_group = is_packagegroup(stash, _file)
        all_items = stash.GetItemsFor(filename=_file,
                                      classifier=Variable.CLASSIFIER,
                                      attribute=Variable.ATTR_VAR,
                                      attributeValue=CONSTANTS.VariablesSuggested)
        for var_ in CONSTANTS.VariablesSuggested:
            if var_ == 'BBCLASSEXTEND':
                # this is better covered by oelint_adv/rule_base/rule_vars_bbclassextends.py
                continue
            if _is_pkg_group and var_ in ['LICENSE', 'CVE_PRODUCT']:
                continue
            items = [x for x in all_items if x.VarName == var_]
            if not any(items):
                res += self.finding(_file, 0, 'Variable \'{var}\' should be set'.format(var=var_), appendix=var_)
        return res
