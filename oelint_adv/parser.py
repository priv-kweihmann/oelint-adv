import re
import collections
import os
try:
    from .cls_item import Item, Comment, Function, PythonBlock, Variable, Include
except (SystemError, ImportError):
    from cls_item import Item, Comment, Function, PythonBlock, Variable, Include

def prepare_lines(_file, lineOffset=0):
    __func_start_regexp__ = r".*(((?P<py>python)|(?P<fr>fakeroot))\s*)*(?P<func>[\w\.\-\+\{\}\$]+)?\s*\(\s*\)\s*\{"
    with open(_file) as i:
        prep_lines = []
        _iter = enumerate(i.readlines())
        for num, line in _iter:
            raw_line = line
            if raw_line.find("\\\n") != -1:
                _, line = _iter.__next__()
                while line.find("\\\n") != -1:
                    raw_line += line
                    _, line = _iter.__next__()
                raw_line += line
            elif re.match(__func_start_regexp__, raw_line):
                _, line = _iter.__next__()
                while line.strip() != "}":
                    raw_line += line
                    _, line = _iter.__next__()
                if line.strip() == "}":
                    raw_line += line
            elif raw_line.strip().startswith("def "):
                _, line = _iter.__next__()
                while (line.startswith(" ") or line.startswith("\t")):
                    raw_line += line
                    _, line = _iter.__next__()
                    if not line.strip():
                        break
            prep_lines.append({"line": num + 1 + lineOffset, "raw": raw_line , "cnt": raw_line.replace("\n", "").replace("\\", "")})
        ##print(prep_lines)
        return prep_lines
    return []

def split_filename_bb(_file):
    __regex_version = r"(?P<recipe>[A-Za-z\-0-9]+)(_(?P<version>.*))*\.(?P<suffix>.*)"


def get_items(stash, _file, lineOffset = 0):
    res = []
    __regex_var = r"^.*?(?P<varname>([A-Z0-9a-z_-]|\$|\{|\})+)(\s*|\t*)(\+|\?)*=(\s*|\t*)(?P<varval>.*)"
    __regex_func = r"^.*(((?P<py>python)|(?P<fr>fakeroot))\s*)*(?P<func>[\w\.\-\+\{\}\$]+)?\s*\(\s*\)\s*\{(?P<funcbody>.*)\s*\}"
    __regex_inherit = r"^.*?inherit(\s+|\t+)(?P<inhname>.+)"
    __regex_comments = r"^.*?#+(?P<body>.*)"
    __regex_python = r"^(\s*|\t*)def(\s+|\t+)(?P<funcname>[a-z0-9_]+)(\s*|\t*)\:.+"
    __regex_include = r"^(\s*|\t*)(include|require)(\s+|\t+)(?P<incname>[A-za-z0-9\-\.]+)"

    _order = collections.OrderedDict([
        ("comment", __regex_comments),
        ("func", __regex_func),
        ("inherit", __regex_inherit),
        ("python", __regex_python),
        ("include", __regex_include),
        ("vars", __regex_var)
    ])

    for line in prepare_lines(_file, lineOffset):
        good = False
        for k, v in _order.items():
            m = re.match(v, line["cnt"], re.MULTILINE)
            if m:
                if k == "python":
                    if any(res) and isinstance(res[-1], PythonBlock):
                        res[-1].Raw += line["raw"]
                    else:
                        res.append(PythonBlock(_file, line["line"],  line["line"] - lineOffset, line["raw"], m.group("funcname")))
                elif k == "vars":
                    res.append(Variable(_file, line["line"], line["line"] - lineOffset, line["raw"], m.group("varname"), m.group("varval")))
                elif k == "func":
                    res.append(Function(_file, line["line"], line["line"] - lineOffset, line["raw"], line["raw"], m.group("funcbody")))
                elif k == "comment":
                    res.append(Comment(_file, line["line"], line["line"] - lineOffset, line["raw"]))
                elif k == "inherit":
                    res.append(Variable(_file, line["line"], line["line"] - lineOffset, line["raw"], "inherit", m.group("inhname")))
                elif k == "include":
                    tmp = stash.AddFile(os.path.abspath(os.path.join(os.path.dirname(_file), m.group("incname"))), lineOffset=line["line"], forcedLink=_file)
                    res.append(Include(_file, line["line"], line["line"] - lineOffset, line["raw"], m.group("incname")))
                    if any(tmp):
                        lineOffset += max([x.InFileLine for x in tmp])
                good = True
            if good:
                break
        if not good:
            res.append(Item(_file, line["line"], line["line"] - lineOffset, line["raw"]))
    return res
