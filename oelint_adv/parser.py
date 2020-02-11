import collections
import os
import re

from oelint_adv.cls_item import Comment
from oelint_adv.cls_item import Function
from oelint_adv.cls_item import Include
from oelint_adv.cls_item import Item
from oelint_adv.cls_item import MissingFile
from oelint_adv.cls_item import PythonBlock
from oelint_adv.cls_item import TaskAdd
from oelint_adv.cls_item import TaskAssignment
from oelint_adv.cls_item import Variable
from oelint_adv.helper_files import find_local_or_in_layer


def prepare_lines(_file, lineOffset=0):
    __func_start_regexp__ = r".*(((?P<py>python)|(?P<fr>fakeroot))\s*)*(?P<func>[\w\.\-\+\{\}\$]+)?\s*\(\s*\)\s*\{"
    try:
        prep_lines = []
        with open(_file) as i:
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
                    stopiter = False
                    while line.strip() != "}" and not stopiter:
                        raw_line += line
                        try:
                            _, line = _iter.__next__()
                        except StopIteration:
                            stopiter = True
                    if line.strip() == "}":
                        raw_line += line
                elif raw_line.strip().startswith("def "):
                    _, line = _iter.__next__()
                    stopiter = False
                    while (line.startswith(" ") or line.startswith("\t")) and not stopiter:
                        raw_line += line
                        try:
                            _, line = _iter.__next__()
                        except StopIteration:
                            stopiter = True
                        if not line.strip():
                            break
                prep_lines.append({"line": num + 1 + lineOffset, "raw": raw_line,
                                   "cnt": raw_line.replace("\n", "").replace("\\", "")})
    except FileNotFoundError:
        pass
    return prep_lines


def get_items(stash, _file, lineOffset=0):
    res = []
    __regex_var = r"^.*?(?P<varname>([A-Z0-9a-z_-]|\$|\{|\})+)(\s*|\t*)(\+|\?)*(:)*=(\s*|\t*)(?P<varval>.*)"
    __regex_func = r"^((?P<py>python)\s+|(?P<fr>fakeroot\s+))*(?P<func>[\w\.\-\+\{\}\$]+)?\s*\(\s*\)\s*\{(?P<funcbody>.*)\s*\}"
    __regex_inherit = r"^.*?inherit(\s+|\t+)(?P<inhname>.+)"
    __regex_comments = r"^.*?#+(?P<body>.*)"
    __regex_python = r"^(\s*|\t*)def(\s+|\t+)(?P<funcname>[a-z0-9_]+)(\s*|\t*)\:.+"
    __regex_include = r"^(\s*|\t*)(?P<statement>include|require)(\s+|\t+)(?P<incname>[A-za-z0-9\-\./]+)"
    __regex_addtask = r"^(\s*|\t*)addtask\s+(?P<func>\w+)\s*((before\s*(?P<before>((.*(?=after))|(.*))))|(after\s*(?P<after>((.*(?=before))|(.*)))))*"
    __regex_taskass = r"^(\s*|\t*)(?P<func>\w+)\[(?P<ident>\w+)\](\s+|\t+)=(\s+|\t+)(?P<varval>.*)"

    _order = collections.OrderedDict([
        ("comment", __regex_comments),
        ("func", __regex_func),
        ("inherit", __regex_inherit),
        ("python", __regex_python),
        ("include", __regex_include),
        ("addtask", __regex_addtask),
        ("taskassign", __regex_taskass),
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
                        res.append(PythonBlock(
                            _file, line["line"], line["line"] - lineOffset, line["raw"], m.group("funcname")))
                elif k == "vars":
                    res.append(Variable(
                        _file, line["line"], line["line"] - lineOffset, line["raw"], m.group("varname"), m.group("varval")))
                elif k == "func":
                    res.append(Function(
                        _file, line["line"], line["line"] -
                        lineOffset, line["raw"],
                        m.group("func"), m.group("funcbody"),
                        m.group("py"), m.group("fr")))
                elif k == "comment":
                    res.append(
                        Comment(_file, line["line"], line["line"] - lineOffset, line["raw"]))
                elif k == "inherit":
                    res.append(Variable(
                        _file, line["line"], line["line"] - lineOffset, line["raw"], "inherit", m.group("inhname")))
                elif k == "taskassign":
                    res.append(TaskAssignment(_file, line["line"], line["line"] - lineOffset, line["raw"], m.group(
                        "func"), m.group("ident"), m.group("varval")))
                elif k == "addtask":
                    _g = m.groupdict()
                    if "before" in _g.keys():
                        _b = _g["before"]
                    else:
                        _b = ""
                    if "after" in _g.keys():
                        _a = _g["after"]
                    else:
                        _a = ""
                    res.append(TaskAdd(
                        _file, line["line"], line["line"] - lineOffset, line["raw"], m.group("func"), _b, _a))
                elif k == "include":
                    _path = find_local_or_in_layer(
                        m.group("incname"), os.path.dirname(_file))
                    if _path:
                        tmp = stash.AddFile(
                            _path, lineOffset=line["line"], forcedLink=_file)
                        if any(tmp):
                            lineOffset += max([x.InFileLine for x in tmp])
                    else:
                        res.append(MissingFile(
                            _file, line["line"], line["line"] - lineOffset, m.group("incname"), m.group("statement")))
                    res.append(Include(
                        _file, line["line"], line["line"] - lineOffset, line["raw"], m.group("incname"), m.group("statement")))
                good = True
            if good:
                break
        if not good:
            res.append(
                Item(_file, line["line"], line["line"] - lineOffset, line["raw"]))
    return res
