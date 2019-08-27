import os
import glob
from oelint_adv.cls_item import *


class Rule():
    def __init__(self, id="", severity="", message=""):
        self.ID = id
        self.Severity = severity
        self.Msg = message

    def check(self, _file, stash):
        return []

    def fix(self, _file, stash):
        return []

    def finding(self, _file, _line, override_msg=None):
        return ["{}:{}:{}:{}:{}".format(os.path.abspath(_file), _line, self.Severity, self.ID, override_msg or self.Msg)]

    def __repr__(self):
        return "{}".format(self.ID)

    def FormatMsg(self, *args):
        return self.Msg.format(*args)

    def OverrideMsg(self, newmsg):
        self.Msg = newmsg


def load_rules():
    res = []
    for file in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rule_*.py")):
        name = os.path.splitext(os.path.basename(file))[0]
        for m in ["oelint_adv." + name]:  # , "." + name, name]:
            try:
                module = __import__(name)
                for member in dir(module):
                    try:
                        if issubclass(getattr(module, member), Rule):
                            inst = getattr(module, member)()
                            if inst.ID:
                                res.append(inst)
                    except:
                        pass
                break
            except Exception as e:
                pass
    return res
