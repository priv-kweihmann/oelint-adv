import sys

__warning_shown = False

if not __warning_shown:
    sys.stderr.write("'oelint_adv.parser' is deprecated. Please use 'oelint_parser.parser' instead\n")
    __warning_shown = True

# provide aliases for legacy imports
from oelint_parser.parser import INLINE_BLOCK as INLINE_BLOCK
