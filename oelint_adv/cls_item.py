import textwrap
import re

from oelint_adv.const_func import KNOWN_FUNCS
from oelint_adv.const_vars import get_known_machines


class Item():
    ATTR_LINE = "Line"
    ATTR_RAW = "Raw"
    ATTR_ORIGIN = "Origin"
    CLASSIFIER = "Item"
    ATTR_SUB = "SubItem"

    def __init__(self, origin, line, infileline, rawtext):
        """constructor

        Arguments:
            origin {str} -- Full path of origin file
            line {int} -- Overall line counter
            infileline {int} -- Line number in file
            rawtext {str} -- Raw input string
        """
        self.Line = line
        self.Raw = rawtext
        self.Links = []
        self.Origin = origin
        self.InFileLine = infileline

    def _safe_linesplit(self, string):
        return re.split(r"\s|\t|\x1b", string)
    
    def get_items(self):
        """Return single items

        Returns:
            list -- lines of raw input
        """
        return self._safe_linesplit(self.Raw)

    def extract_sub(self, name):
        """Extract modifiers

        Arguments:
            name {str} -- input string

        Returns:
            tuple -- clean variable name, modifiers, package specific modifiers
        """
        chunks = name.split("_")
        _suffix = []
        _var = []
        _pkgspec = []
        for i in chunks:
            tmp = ""
            if "-" in i:
                # just use the prefix in case a dash is found
                # that addresses things like FILES_${PN}-dev
                tmp = "-" + "-".join(i.split("-")[1:])
                i = i.split("-")[0]
            if re.match("^[a-z0-9{}$]+$", i):
                _suffix.append(i + tmp)
            else:
                _var.append(i + tmp)
        _var = [x for x in _var if x]
        _suffix = [x for x in _suffix if x]
        if not _var and _suffix:
            # special case for pkg-functions
            _var = _suffix
            _suffix = []
        return ("_".join(_var), "_".join(_suffix), _pkgspec)

    def extract_sub_func(self, name):
        """Extract modifiers for functions

        Arguments:
            name {str} -- input value

        Returns:
            tuple -- clean function name, modifiers
        """
        chunks = name.split("_")
        _marker = ["append", "prepend", "class-native",
                   "class-cross", "class-target", "remove"]
        _suffix = []
        _var = []
        for i in chunks:
            if i in _marker or "_".join(_var) in KNOWN_FUNCS:
                _suffix = chunks[chunks.index(i):]
                break
            else:
                _var.append(i)
        _var = [x for x in _var if x]
        _suffix = [x for x in _suffix if x]
        return ("_".join(_var), "_".join(_suffix))

    def IsFromAppend(self):
        """Item originates from a bbappend

        Returns:
            bool -- True if coming from a bbappend
        """
        return self.Origin.endswith(".bbappend")

    def AddLink(self, _file):
        """Links files to each other in stash

        Arguments:
            _file {str} -- Full path of file to link against
        """
        self.Links.append(_file)
        self.Links = list(set(self.Links))

    def GetAttributes(self):
        """Get all public attributes of this class

        Returns:
            dict -- all public attributes and their values
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __repr__(self):
        return "{} -- {}\n".format(self.__class__.__name__, self.GetAttributes())


class Variable(Item):
    ATTR_VAR = "VarName"
    ATTR_VARVAL = "VarValue"
    ATTR_VARVALSTRIPPED = "VarValueStripped"
    CLASSIFIER = "Variable"
    VAR_VALID_OPERATOR = [" = ", " += ",
                          " ?= ", " ??= ", " := ", " .= ", " =+ ", " =. "]

    def __init__(self, origin, line, infileline, rawtext, name, value, operator, flag):
        """constructor

        Arguments:
            origin {str} -- Full path to file of origin
            line {int} -- Overall line counter
            infileline {int} -- Line counter in the particular file
            rawtext {str} -- Raw string
            name {str} -- Variable name
            value {str} -- Variable value
            operator {str} -- Operation performed to the variable
            flag {str} -- Optional variable flag
        """
        super().__init__(origin, line, infileline, rawtext)
        if "inherit" != name:
            self.VarName, self.SubItem, self.PkgSpec = self.extract_sub(name)
            self.SubItem += " ".join(self.PkgSpec)
        else:
            self.VarName = name
            self.SubItem = ""
            self.PkgSpec = []
        self.SubItems = [x for x in self.SubItem.split(
            "_") + self.PkgSpec if x]
        self.VarValue = value
        self.VarOp = operator
        self.Flag = flag or ""
        self.VarValueStripped = self.VarValue.strip().lstrip('"').rstrip('"')

    def IsAppend(self):
        """Check if operation is an append

        Returns:
            bool -- True is variable is appended
        """
        return self.VarOp in [" += ", " =+ ", " =. ", " .= "] or "append" in self.SubItems

    def AppendOperation(self):
        """Get variable modifiers

        Returns:
            list -- list could contain any combination of 'append', ' += ', 'prepend' and 'remove'
        """
        res = []
        if self.VarOp in [" += " , " .= ", " =+ ", " =. "]:
            res.append(self.VarOp)
        if "append" in self.SubItems:
            res.append("append")
        if "prepend" in self.SubItems:
            res.append("prepend")
        if "remove" in self.SubItems:
            res.append("remove")
        return res
    
    def get_items(self):
        """Get items of variable value

        Returns:
            list -- clean list of items in variable value
        """
        return self._safe_linesplit(self.VarValue.strip('"'))

    def IsMultiLine(self):
        """Check if variable has a multiline assignment

        Returns:
            bool -- True if multiline
        """
        return "\\" in self.Raw

    def GetMachineEntry(self):
        """Get machine specific entries in variable

        Returns:
            str -- machine specific modifier of variable or ""
        """
        for x in self.SubItems:
            if x not in ["append", "prepend", "class-native", "class-nativesdk", "class-cross", "class-target", "remove", "machine"] + self.PkgSpec:
                return x
        return ""


class Comment(Item):
    CLASSIFIER = "Comment"

    def __init__(self, origin, line, infileline, rawtext):
        """constructor

        Arguments:
            origin {str} -- Full path to file of origin
            line {int} -- Overall line counter
            infileline {int} -- Line counter in the particular file
            rawtext {str} -- Raw string
        """
        super().__init__(origin, line, infileline, rawtext)
    
    def get_items(self):
        """Get single lines of block

        Returns:
            list -- single lines of comment block
        """
        return self.Raw.split("\n")

class Include(Item):
    CLASSIFIER = "Include"
    ATTR_INCNAME = "IncName"
    ATTR_STATEMENT = "Statement"

    def __init__(self, origin, line, infileline, rawtext, incname, statement):
        """constructor

        Arguments:
            origin {str} -- Full path to file of origin
            line {int} -- Overall line counter
            infileline {int} -- Line counter in the particular file
            rawtext {str} -- Raw string
            incname {str} -- raw name of the include file
            statement {str} -- either include or require
        """
        super().__init__(origin, line, infileline, rawtext)
        self.IncName = incname
        self.Statement = statement
    
    def get_items(self):
        """Get items

        Returns:
            list -- include name, include statement
        """
        return [self.IncName, self.Statement]


class Function(Item):
    ATTR_FUNCNAME = "FuncName"
    ATTR_FUNCBODY = "FuncBody"
    CLASSIFIER = "Function"

    def __init__(self, origin, line, infileline, rawtext, name, body, python=False, fakeroot=False):
        """[summary]

        Arguments:
            origin {str} -- Full path to file of origin
            line {int} -- Overall line counter
            infileline {int} -- Line counter in the particular file
            rawtext {str} -- Raw string
            name {str} -- Raw function name
            body {str} -- Function body

        Keyword Arguments:
            python {bool} -- python function according to parser (default: {False})
            fakeroot {bool} -- uses fakeroot (default: {False})
        """
        super().__init__(origin, line, infileline, rawtext)
        self.IsPython = python is not None
        self.IsFakeroot = fakeroot is not None
        name = name or ""
        self.FuncName, self.SubItem = self.extract_sub_func(name.strip())
        self.SubItems = self.SubItem.split("_")
        self.FuncBody = body
        self.FuncBodyStripped = body.replace(
            "{", "").replace("}", "").replace("\n", "").strip()
        self.FuncBodyRaw = textwrap.dedent(
            rawtext[rawtext.find("{") + 1:].rstrip().rstrip("}"))

    def GetMachineEntry(self):
        """Get machine specific modifiers

        Returns:
            str -- machine specific modifier or ""
        """
        for x in self.SubItems:
            if x not in ["append", "prepend", "class-native", "class-cross", "class-target", "remove", "machine"]:
                return x
        return ""

    def IsAppend(self):
        """Return if function appends another function

        Returns:
            bool -- True is append or prepend operation
        """
        return any([x in ["append", "prepend"] for x in self.SubItems])

    def get_items(self):
        """Get items of function body

        Returns:
            list -- single lines of function body
        """
        return self.FuncBodyRaw.split("\n")


class PythonBlock(Item):
    ATTR_FUNCNAME = "FuncName"
    CLASSIFIER = "PythonBlock"

    def __init__(self, origin, line, infileline, rawtext, name):
        """constructor

        Arguments:
            origin {str} -- Full path to file of origin
            line {int} -- Overall line counter
            infileline {int} -- Line counter in the particular file
            rawtext {str} -- Raw string
            name {str} -- Function name
        """
        super().__init__(origin, line, infileline, rawtext)
        self.FuncName = name
    
    def get_items(self):
        """Get lines of function body

        Returns:
            list -- lines of function body
        """
        return self.Raw.split("\n")


class TaskAssignment(Item):
    ATTR_FUNCNAME = "FuncName"
    ATTR_VAR = "VarName"
    ATTR_VARVAL = "VarValue"
    CLASSIFIER = "TaskAssignment"

    def __init__(self, origin, line, infileline, rawtext, name, ident, value):
        """constructor

        Arguments:
            origin {str} -- Full path to file of origin
            line {int} -- Overall line counter
            infileline {int} -- Line counter in the particular file
            rawtext {str} -- Raw string
            name {str} -- name of task to be modified
            ident {str} -- task flag
            value {str} -- value of modification
        """
        super().__init__(origin, line, infileline, rawtext)
        self.FuncName = name
        self.VarName = ident
        self.VarValue = value
    
    def get_items(self):
        """Get items

        Returns:
            list -- function name, flag, modification value
        """
        return [self.FuncName, self.VarName, self.VarValue]


class TaskAdd(Item):
    ATTR_FUNCNAME = "FuncName"
    ATTR_BEFORE = "Before"
    ATTR_AFTER = "After"
    CLASSIFIER = "TaskAdd"

    def __init__(self, origin, line, infileline, rawtext, name, before="", after=""):
        """constructor

        Arguments:
            origin {str} -- Full path to file of origin
            line {int} -- Overall line counter
            infileline {int} -- Line counter in the particular file
            rawtext {str} -- Raw string
            name {str} -- name of task to be executed

        Keyword Arguments:
            before {str} -- before statement (default: {""})
            after {str} -- after statement (default: {""})
        """
        super().__init__(origin, line, infileline, rawtext)
        self.FuncName = name
        self.Before = [x for x in (before or "").split(" ") if x]
        self.After = [x for x in (after or "").split(" ") if x]

    def get_items(self):
        """get items

        Returns:
            list -- function name, all before statements, all after statements
        """
        return [self.FuncName] + self.Before + self.After

class MissingFile(Item):
    ATTR_FILENAME = "Filename"
    ATTR_STATEMENT = "Statement"
    CLASSIFIER = "MissingFile"

    def __init__(self, origin, line, infileline, filename, statement):
        """constructor

        Arguments:
            origin {str} -- Full path to file of origin
            line {int} -- Overall line counter
            infileline {int} -- Line counter in the particular file
            filename {str} -- filename of the file that can't be found
            statement {str} -- either include or require
        """
        super().__init__(origin, line, infileline, "")
        self.Filename = filename
        self.Statement = statement

    def get_items(self):
        return [self.Filename, self.Statement]
