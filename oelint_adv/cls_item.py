import sys

__warning_shown = False

if not __warning_shown:
    sys.stderr.write("'oelint_adv.cls_item' is deprecated. Please use 'oelint_parser.cls_item' instead\n")
    __warning_shown = True

# provide aliases for legacy imports
from oelint_parser.cls_item import Comment as Comment
from oelint_parser.cls_item import Include as Include
from oelint_parser.cls_item import Item as Item
from oelint_parser.cls_item import MissingFile as MissingFile
from oelint_parser.cls_item import PythonBlock as PythonBlock
from oelint_parser.cls_item import TaskAdd as TaskAdd
from oelint_parser.cls_item import TaskAssignment as TaskAssignment
from oelint_parser.cls_item import Variable as Variable
