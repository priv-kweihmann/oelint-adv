import textwrap


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
        if len(chunks) > 2 and chunks[-1].islower():
            return ("_".join(chunks[:-1]), chunks[-1])
        return ("_".join(chunks), "")

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
    VARIABLE_APPEND_NEEDLES = ["+="]

    def __init__(self, origin, line, infileline, rawtext, name, value):
        super().__init__(origin, line, infileline, rawtext)
        self.VarName, self.SubItem = self.extract_sub(name)
        self.VarValue = value
        self.VarValueStripped = self.VarValue.strip().lstrip('"').rstrip('"')

    def IsAppend(self):
        return any([x for x in Variable.VARIABLE_APPEND_NEEDLES if self.Raw.find(x) != -1]) \
               or self.Raw.find("_append") != -1

    def IsMultiLine(self):
        return "\\" in self.Raw


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
        self.FuncName, self.SubItem = self.extract_sub(name.strip())
        if self.SubItem not in ["", "append", "remove", "class-target", "class-native"]:
            self.FuncName += "_" + self.SubItem
        self.FuncBody = body
        self.FuncBodyStripped = body.replace(
            "{", "").replace("}", "").replace("\n", "").strip()
        self.FuncBodyRaw = textwrap.dedent(
            rawtext[rawtext.find("{") + 1:].rstrip().rstrip("}"))


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
