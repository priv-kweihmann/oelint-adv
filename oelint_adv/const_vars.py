import sys

__warning_shown = False

if not __warning_shown:
    sys.stderr.write("'oelint_adv.const_vars' is deprecated. Please use 'oelint_parser.const_vars' instead\n")
    __warning_shown = True

# provide aliases for legacy imports
from oelint_parser.const_vars import get_base_varset as get_base_varset
from oelint_parser.const_vars import get_constantfile as get_constantfile
from oelint_parser.const_vars import get_known_machines as get_known_machines
from oelint_parser.const_vars import get_known_mirrors as get_known_mirrors
from oelint_parser.const_vars import get_known_vars as get_known_vars
from oelint_parser.const_vars import get_mandatory_vars as get_mandatory_vars
from oelint_parser.const_vars import get_protected_append_vars as get_protected_append_vars
from oelint_parser.const_vars import get_protected_vars as get_protected_vars
from oelint_parser.const_vars import get_rulefile as get_rulefile
from oelint_parser.const_vars import get_suggested_vars as get_suggested_vars
from oelint_parser.const_vars import KNOWN_MACHINES as KNOWN_MACHINES
from oelint_parser.const_vars import KNOWN_MIRRORS as KNOWN_MIRRORS
from oelint_parser.const_vars import KNOWN_VARS as KNOWN_VARS
from oelint_parser.const_vars import MANDATORY_VARS as MANDATORY_VARS
from oelint_parser.const_vars import SUGGESTED_VARS as SUGGESTED_VARS
from oelint_parser.const_vars import VAR_ORDER as VAR_ORDER
from oelint_parser.const_vars import VAR_PROTECTED as VAR_PROTECTED
from oelint_parser.const_vars import VAR_PROTECTED_APPEND as VAR_PROTECTED_APPEND
