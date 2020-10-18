import sys

__warning_shown = False

if not __warning_shown:
    sys.stderr.write("'oelint_adv.helper_files' is deprecated. Please use 'oelint_parser.helper_files' instead\n")
    __warning_shown = True

# provide aliases for legacy imports
from oelint_parser.helper_files import expand_term as expand_term
from oelint_parser.helper_files import find_local_or_in_layer as find_local_or_in_layer
from oelint_parser.helper_files import get_files as get_files
from oelint_parser.helper_files import get_known_mirrors as get_known_mirrors
from oelint_parser.helper_files import get_layer_root as get_layer_root
from oelint_parser.helper_files import get_scr_components as get_scr_components
from oelint_parser.helper_files import get_valid_named_resources as get_valid_named_resources
from oelint_parser.helper_files import get_valid_package_names as get_valid_package_names
from oelint_parser.helper_files import guess_base_recipe_name as guess_base_recipe_name
from oelint_parser.helper_files import guess_recipe_name as guess_recipe_name
from oelint_parser.helper_files import guess_recipe_version as guess_recipe_version
from oelint_parser.helper_files import safe_linesplit as safe_linesplit
