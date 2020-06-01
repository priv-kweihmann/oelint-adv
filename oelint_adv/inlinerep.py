import re

def bb_utils_contains(_in):
    m = re.match(r"(.*)bb\.utils\.contains\(.*?,\s*.*?,\s*(.*?),\s*.*?,\s*.\)", _in)
    if m:
        return m.group(1) + m.group(2).strip("\"'")
    return None

def bb_utils_contains_any(_in):
    m = re.match(r"(.*)bb\.utils\.contains_any\(.*?,\s*.*?,\s*(.*?),\s*.*?,\s*.\)", _in)
    if m:
        return m.group(1) + m.group(2).strip("\"'")
    return None

def oe_utils_conditional(_in):
    m = re.match(r"(.*)oe\.utils\.conditional\(.*?,\s*.*?,\s*(.*?),\s*.*?,\s*.\)", _in)
    if m:
        return m.group(1) + m.group(2).strip("\"'")
    return None

def oe_utils_ifelse(_in):
    m = re.match(r"(.*)oe\.utils\.ifelse\(.*?,\s*(.*?),\s*.*?\)", _in)
    if m:
        return m.group(1) + m.group(2).strip("\"'")
    return None

def inlinerep(_in):
    _clean_in = _in.lstrip("${@").rstrip("}")
    for x in [bb_utils_contains(_clean_in), 
              bb_utils_contains_any(_clean_in),
              oe_utils_conditional(_clean_in),
              oe_utils_ifelse(_clean_in)]:
        if x:
            return x
    return None