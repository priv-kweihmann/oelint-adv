import sys

__warning_shown = False

if not __warning_shown:
    sys.stderr.write("'oelint_adv.const_func' is deprecated. Please use 'oelint_parser.const_func' instead\n")
    __warning_shown = True

# provide aliases for legacy imports
from oelint_parser.const_func import FUNC_ORDER as FUNC_ORDER
from oelint_parser.const_func import KNOWN_FUNCS as KNOWN_FUNCS
