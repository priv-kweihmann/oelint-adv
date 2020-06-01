import collections
import os
import re

from oelint_adv.cls_item import Comment
from oelint_adv.cls_item import Function
from oelint_adv.cls_item import Include
from oelint_adv.cls_item import Item
from oelint_adv.cls_item import PythonBlock
from oelint_adv.cls_item import TaskAdd
from oelint_adv.cls_item import TaskAssignment
from oelint_adv.cls_item import Variable
from oelint_adv.helper_files import find_local_or_in_layer, expand_term
from oelint_adv.inlinerep import inlinerep

INLINE_BLOCK = "!!!inlineblock!!!"

def get_full_scope(_string, offset, _sstart, _send):
    scopelevel = 0
    pos = 0
    for c in _string[offset:]:
        if c == _sstart:
            scopelevel += 1
        elif c == _send:
            scopelevel -= 1
        pos += 1
        if scopelevel < 0:
            break
    return _string[:pos+offset]


def prepare_lines_subparser(_iter, lineOffset, num, line, raw_line=None):
    __func_start_regexp__ = r".*(((?P<py>python)|(?P<fr>fakeroot))\s*)*(?P<func>[\w\.\-\+\{\}\$]+)?\s*\(\s*\)\s*\{"
    res = []
    raw_line = raw_line or line
    if raw_line.find("\\\n") != -1:
        _, line = _iter.__next__()
        while line.find("\\\n") != -1:
            raw_line += line
            _, line = _iter.__next__()
        raw_line += line
    elif re.match(__func_start_regexp__, raw_line):
        _, line = _iter.__next__()
        stopiter = False
        scope_level = 0
        while not stopiter:
            raw_line += line
            if "{" in line:
                scope_level += 1
            if "}" in line:
                scope_level -= 1
            try:
                _, line = _iter.__next__()
            except StopIteration:
                stopiter = True
            if line.strip() == "}" and not scope_level:
                stopiter = True
        if line.strip() == "}":
            raw_line += line
    elif raw_line.strip().startswith("def "):
        stopiter = False
        while not stopiter:
            try:
                _, line = _iter.__next__()
            except StopIteration:
                stopiter = True
            if re.match("^[A-Za-z0-9#]+", line) or stopiter:
                if not stopiter:
                    res += prepare_lines_subparser(_iter,
                                                lineOffset, num, line)
                break
            if line.startswith("def "):
                raw_line = line
                res += prepare_lines_subparser(_iter,
                                               lineOffset, num, line, raw_line=raw_line)
                break
            raw_line += line

    while raw_line.find("${@") != -1:
        _inline_block = raw_line.find("${@")
        repl = get_full_scope(raw_line[_inline_block:], len("${@"), "{", "}")
        _repl = inlinerep(repl) or INLINE_BLOCK
        raw_line = raw_line.replace(repl, _repl)
    res.append({"line": num + 1 + lineOffset, "raw": raw_line,
                "cnt": raw_line.replace("\n", "").replace("\\", chr(0x1b))})
    return res


def prepare_lines(_file, lineOffset=0):
    try:
        prep_lines = []
        with open(_file) as i:
            _iter = enumerate(i.readlines())
            for num, line in _iter:
                prep_lines += prepare_lines_subparser(
                    _iter, lineOffset, num, line)
    except FileNotFoundError:
        pass
    return prep_lines


def get_items(stash, _file, lineOffset=0):
    res = []
    __regex_var = r"^(?P<varname>([A-Z0-9a-z_-]|\$|\{|\})+?)(\[(?P<ident>(\w|-)+)\])*(?P<varop>(\s|\t)*(\+|\?|\:|\.)*=(\+|\.)*(\s|\t)*)(?P<varval>.*)"
    __regex_func = r"^((?P<py>python)\s+|(?P<fr>fakeroot\s+))*(?P<func>[\w\.\-\+\{\}\$]+)?\s*\(\s*\)\s*\{(?P<funcbody>.*)\s*\}"
    __regex_inherit = r"^.*?inherit(\s+|\t+)(?P<inhname>.+)"
    __regex_comments = r"^(\s|\t)*#+\s*(?P<body>.*)"
    __regex_python = r"^(\s*|\t*)def(\s+|\t+)(?P<funcname>[a-z0-9_]+)(\s*|\t*)\(.*\)\:"
    __regex_include = r"^(\s*|\t*)(?P<statement>include|require)(\s+|\t+)(?P<incname>[A-za-z0-9\-\./\$\{\}]+)"
    __regex_addtask = r"^(\s*|\t*)addtask\s+(?P<func>\w+)\s*((before\s*(?P<before>((.*(?=after))|(.*))))|(after\s*(?P<after>((.*(?=before))|(.*)))))*"
    __regex_taskass = r"^(\s*|\t*)(?P<func>[a-z0-9_-]+)\[(?P<ident>\w+)\](\s+|\t+)=(\s+|\t+)(?P<varval>.*)"

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

    includeOffset = 0

    for line in prepare_lines(_file, lineOffset):
        good = False
        for k, v in _order.items():
            m = re.match(v, line["cnt"], re.MULTILINE)
            if m:
                if k == "python":
                    res.append(PythonBlock(
                        _file, line["line"] + includeOffset, line["line"] - lineOffset, line["raw"], m.group("funcname")))
                    good = True
                    break
                elif k == "vars":
                    res.append(Variable(
                        _file, line["line"] + includeOffset, line["line"] -
                        lineOffset, line["raw"], m.group(
                            "varname"), m.group("varval"),
                        m.group("varop"), m.group("ident")))
                    good = True
                    break
                elif k == "func":
                    res.append(Function(
                        _file, line["line"] + includeOffset, line["line"] -
                        lineOffset, line["raw"],
                        m.group("func"), m.group("funcbody"),
                        m.group("py"), m.group("fr")))
                    good = True
                    break
                elif k == "comment":
                    res.append(
                        Comment(_file, line["line"] + includeOffset, line["line"] - lineOffset, line["raw"]))
                    good = True
                    break
                elif k == "inherit":
                    res.append(Variable(
                        _file, line["line"] + includeOffset, line["line"] -
                        lineOffset, line["raw"], "inherit", m.group("inhname"),
                        "", ""))
                    good = True
                    break
                elif k == "taskassign":
                    res.append(TaskAssignment(_file, line["line"] + includeOffset, line["line"] - lineOffset, line["raw"], m.group(
                        "func"), m.group("ident"), m.group("varval")))
                    good = True
                    break
                elif k == "addtask":
                    # treat the following as variables
                    if any([m.group("func").startswith(x) for x in ['pkg_preinst', 'pkg_postinst', 'pkg_prerm', 'pkg_postrm']]):
                        continue
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
                        _file, line["line"] + includeOffset, line["line"] - lineOffset, line["raw"], m.group("func"), _b, _a))
                    break
                elif k == "include":
                    _path = find_local_or_in_layer(
                        expand_term(stash, _file, m.group("incname")), os.path.dirname(_file))
                    if _path:
                        tmp = stash.AddFile(
                            _path, lineOffset=line["line"], forcedLink=_file)
                        if any(tmp):
                            includeOffset += max([x.InFileLine for x in tmp])
                    res.append(Include(
                        _file, line["line"], line["line"] - lineOffset, line["raw"], m.group("incname"), m.group("statement")))
                    good = True
                    break
        if not good:
            res.append(
                Item(_file, line["line"], line["line"] - lineOffset, line["raw"]))
    print(res)
    return res
