import textwrap
import re

from oelint_adv.const_func import KNOWN_FUNCS


class Item():
    ATTR_LINE = "Line"
    ATTR_RAW = "Raw"
    ATTR_ORIGIN = "Origin"
    CLASSIFIER = "Item"
    ATTR_SUB = "SubItem"

    def __init__(self, origin, line, infileline, rawtext):
        self.Line = line
        self.Raw = rawtext
        self.Links = []
        self.Origin = origin
        self.InFileLine = infileline

    def extract_sub(self, name):
        chunks = name.split("_")
        _suffix = []
        _var = []
        _pkgspec = []
        for i in chunks:
            if "-" in i:
                # just use the prefix in case a dash is found
                # that addresses things like FILES_${PN}-dev
                _pkgspec.append("-".join(i.split("-")[1:]))
                i = i.split("-")[0]
            if re.match("^[a-z0-9{}$]+$", i):
                _suffix.append(i)
            else:
                _var.append(i)
        _var = [x for x in _var if x]
        _suffix = [x for x in _suffix if x]
        if not _var and _suffix:
            # special case for pkg-functions
            _var = _suffix
            _suffix = []
        return ("_".join(_var), "_".join(_suffix), _pkgspec)

    def extract_sub_func(self, name):
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
        return self.Origin.endswith(".bbappend")

    def AddLink(self, _file):
        self.Links.append(_file)
        self.Links = list(set(self.Links))

    def GetAttributes(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def GetRawCleaned(self, chars="\t\n\r"):
        res = self.Raw
        for c in chars:
            res = res.replace(c, " ")
        return res

    def __repr__(self):
        return "{} -- {}\n".format(self.__class__.__name__, self.GetAttributes())


class Variable(Item):
    ATTR_VAR = "VarName"
    ATTR_VARVAL = "VarValue"
    ATTR_VARVALSTRIPPED = "VarValueStripped"
    CLASSIFIER = "Variable"
    VAR_VALID_OPERATOR = [" = ", " += ",
                          " ?= ", " ??= ", " := ", " .= ", " =+ "]

    def __init__(self, origin, line, infileline, rawtext, name, value, operator, flag):
        super().__init__(origin, line, infileline, rawtext)
        if "inherit" != name:
            self.VarName, self.SubItem, self.PkgSpec = self.extract_sub(name)
            self.SubItem += " ".join(self.PkgSpec)
        else:
            self.VarName = name
            self.SubItem = ""
            self.PkgSpec = []
        self.SubItems = [x for x in self.SubItem.split("_") + self.PkgSpec if x]
        self.VarValue = value
        self.VarOp = operator
        self.Flag = flag or ""
        self.VarValueStripped = self.VarValue.strip().lstrip('"').rstrip('"')

    def IsAppend(self):
        return self.VarOp in [" += "] or "append" in self.SubItems

    def AppendOperation(self):
        res = []
        if self.VarOp in [" += "]:
            res.append(self.VarOp)
        if "append" in self.SubItems:
            res.append("append")
        if "prepend" in self.SubItems:
            res.append("prepend")
        if "remove" in self.SubItems:
            res.append("remove")
        return res

    def IsMultiLine(self):
        return "\\" in self.Raw

    def GetMachineEntry(self):
        for x in self.SubItems:
            if x not in ["append", "prepend", "class-native", "class-cross", "class-target", "remove", "machine"] + self.PkgSpec:
                if not x.startswith("libc"):
                    return x
        return ""


class Comment(Item):
    CLASSIFIER = "Comment"

    def __init__(self, origin, line, infileline, rawtext):
        super().__init__(origin, line, infileline, rawtext)


class Include(Item):
    CLASSIFIER = "Include"
    ATTR_INCNAME = "IncName"
    ATTR_STATEMENT = "Statement"

    def __init__(self, origin, line, infileline, rawtext, incname, statement):
        super().__init__(origin, line, infileline, rawtext)
        self.IncName = incname
        self.Statement = statement


class Function(Item):
    ATTR_FUNCNAME = "FuncName"
    ATTR_FUNCBODY = "FuncBody"
    CLASSIFIER = "Function"

    def __init__(self, origin, line, infileline, rawtext, name, body, python=False, fakeroot=False):
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
        for x in self.SubItems:
            if x not in ["append", "prepend", "class-native", "class-cross", "class-target", "remove", "machine"]:
                return x
        return ""

    def IsAppend(self):
        return any([x in ["append", "prepend"] for x in self.SubItems])


class PythonBlock(Item):
    ATTR_FUNCNAME = "FuncName"
    CLASSIFIER = "PythonBlock"

    def __init__(self, origin, line, infileline, rawtext, name):
        super().__init__(origin, line, infileline, rawtext)
        self.FuncName = name


class TaskAssignment(Item):
    ATTR_FUNCNAME = "FuncName"
    ATTR_VAR = "VarName"
    ATTR_VARVAL = "VarValue"
    CLASSIFIER = "TaskAssignment"

    def __init__(self, origin, line, infileline, rawtext, name, ident, value):
        super().__init__(origin, line, infileline, rawtext)
        self.FuncName = name
        self.VarName = ident
        self.VarValue = value


class TaskAdd(Item):
    ATTR_FUNCNAME = "FuncName"
    ATTR_BEFORE = "Before"
    ATTR_AFTER = "After"
    CLASSIFIER = "TaskAdd"

    def __init__(self, origin, line, infileline, rawtext, name, before="", after=""):
        super().__init__(origin, line, infileline, rawtext)
        self.FuncName = name
        self.Before = [x for x in (before or "").split(" ") if x]
        self.After = [x for x in (after or "").split(" ") if x]


class MissingFile(Item):
    ATTR_FILENAME = "Filename"
    ATTR_STATEMENT = "Statement"
    CLASSIFIER = "MissingFile"

    def __init__(self, origin, line, infileline, filename, statement):
        super().__init__(origin, line, infileline, "")
        self.Filename = filename
        self.Statement = statement
