import argparse
import json
import os
import re
import sys

from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import load_rules
from oelint_adv.color import set_color
from oelint_adv.rule_file import set_noinfo
from oelint_adv.rule_file import set_nowarn
from oelint_adv.rule_file import set_rulefile
from oelint_adv.rule_file import set_suppressions

sys.path.append(os.path.abspath(os.path.join(__file__, "..")))


def create_argparser():
    parser = argparse.ArgumentParser(prog='oelint-adv',
        description='Advanced OELint - Check bitbake recipes against OECore styleguide')
    parser.add_argument("--suppress", default=[],
                        action="append", help="Rules to suppress")
    parser.add_argument("--output", default=sys.stderr,
                        help="Where to flush the findings (default: stderr)")
    parser.add_argument("--fix", action="store_true", default=False,
                        help="Automatically try to fix the issues")
    parser.add_argument("--nobackup", action="store_true", default=False,
                        help="Don't create backup file when auto fixing")
    parser.add_argument("--addrules", nargs="+", default=[],
                        help="Additional non-default rulessets to add")
    parser.add_argument("--customrules", nargs="+", default=[],
                        help="Additional directories to parse for rulessets")
    parser.add_argument("--rulefile", default=None,
                        help="Rulefile")
    parser.add_argument("--constantfile", default=None, help="Constantfile")
    parser.add_argument("--color", action="store_true", default=False,
                        help="Add color to the output based on the severity")
    parser.add_argument("--quiet", action="store_true", default=False,
                        help="Print findings only")
    parser.add_argument("--noinfo", action="store_true", default=False,
                        help="Don't print information level findings")
    parser.add_argument("--nowarn", action="store_true", default=False,
                        help="Don't print warning level findings")
    parser.add_argument("--constantmods", default=[], nargs='+',
                        help="""
                             Modifications to the constant db.
                             prefix with:
                             + - to add to DB,
                             - - to remove from DB,
                             None - to override DB
                            """)
    parser.add_argument("--print-rulefile", action="store_true", default=False,
                        help="Print loaded rules as a rulefile and exit")
    parser.add_argument("--exit-zero", action="store_true", default=False,
        help="Always return a 0 (non-error) status code, even if lint errors are found")
    parser.add_argument("files", nargs='*', help="File to parse")

    return parser


def parse_arguments():
    return create_argparser().parse_args() # pragma: no cover

def arguments_post(args):
    if args.files == [] and not args.print_rulefile:
        raise argparse.ArgumentTypeError("no input files")

    if args.rulefile:
        try:
            with open(args.rulefile) as i:
                set_rulefile(json.load(i))
        except (FileNotFoundError, json.JSONDecodeError):
            raise argparse.ArgumentTypeError("'rulefile' is not a valid file")

    if args.constantfile:
        try:
            with open(args.constantfile) as i:
                CONSTANTS.AddFromConstantFile(json.load(i))
        except (FileNotFoundError, json.JSONDecodeError):
            raise argparse.ArgumentTypeError(
                "'constantfile' is not a valid file")

    for mod in args.constantmods:
        try:
            with open(mod.lstrip('+-')) as _in:
                _cnt = json.load(_in)
            if mod.startswith("+"):
                CONSTANTS.AddConstants(_cnt)
            elif mod.startswith("-"):
                CONSTANTS.RemoveConstants(_cnt)
            else:
                CONSTANTS.OverrideConstants(_cnt)
        except (FileNotFoundError, json.JSONDecodeError):
            raise argparse.ArgumentTypeError(
                "mod file '{file}' is not a valid file".format(file=mod))

    if args.color:
        set_color(True)
    if args.nowarn:
        set_nowarn(True)
    if args.noinfo:
        set_noinfo(True)
    set_suppressions(args.suppress)
    return args


def group_files(files):
    # in case multiple bb files are passed at once we might need to group them to
    # avoid having multiple, potentially wrong hits of include files shared across
    # the bb files in the stash
    res = {}
    for f in files:
        _filename, _ext = os.path.splitext(f)
        if _ext not in [".bb"]:
            continue
        _filename_key = "_".join(os.path.basename(_filename).split("_")[:-1]).replace("%", "")
        if not _filename_key in res: # pragma: no cover
            res[_filename_key] = set()
        res[_filename_key].add(f)

    # second round now for the bbappend files
    for f in files:
        _filename, _ext = os.path.splitext(f)
        if _ext not in [".bbappend"]:
            continue
        _match = False
        for k, v in res.items():
            _needle = ".*/" + os.path.basename(_filename).replace("%", ".*")
            if any(re.match(_needle, x) for x in v):
                v.add(f)
                _match = True
                break
        if not _match:
            _filename_key = "_".join(os.path.basename(_filename).split("_")[:-1]).replace("%", "")
            if not _filename_key in res: # pragma: no cover
                res[_filename_key] = set()
            res[_filename_key].add(f)

    # as sets are unordered, we convert them to sorted lists at this point
    # order is like the files have been passed via CLI
    for k, v in res.items():
        res[k] = sorted(v, key=lambda index: files.index(index))

    return res.values()

def print_rulefile(args):
    rules = [x for x in load_rules(args,
        add_rules=args.addrules, add_dirs=args.customrules)]
    ruleset = {}
    for r in rules:
        ruleset.update(r.GetRulefileEntries())
    print(json.dumps(ruleset, indent=2))

def run(args):
    try:
        rules = [x for x in load_rules(args,
            add_rules=args.addrules, add_dirs=args.customrules)]
        _loadedIDs = []
        for r in rules:
            _loadedIDs += r.GetIDs()
        if not args.quiet:
            print("Loaded rules:\n\t{}".format("\n\t".join(sorted(_loadedIDs))))
        issues = []
        fixedfiles = []
        groups = group_files(args.files)
        for group in groups:
            stash = Stash(args)
            for f in group:
                try:
                    stash.AddFile(f)
                except FileNotFoundError as e: # pragma: no cover
                    if not args.quiet: # pragma: no cover
                        print("Can't open/read: {}".format(e)) # pragma: no cover

            stash.Finalize()

            _files = list(set(stash.GetRecipes() + stash.GetLoneAppends()))
            for index, f in enumerate(_files):
                for r in rules:
                    if not r.OnAppend and f.endswith(".bbappend"):
                        continue
                    if r.OnlyAppend and not f.endswith(".bbappend"):
                        continue
                    if args.fix:
                        fixedfiles += r.fix(f, stash)
                    issues += r.check(f, stash)
            fixedfiles = list(set(fixedfiles))
            for f in fixedfiles:
                _items = [f] + stash.GetLinksForFile(f)
                for i in _items:
                    items = stash.GetItemsFor(filename=i, nolink=True)
                    if not args.nobackup:
                        os.rename(i, i + ".bak") # pragma: no cover
                    with open(i, "w") as o:
                        o.write("".join([x.RealRaw for x in items]))
                        if not args.quiet:
                            print("{}:{}:{}".format(os.path.abspath(i),  # pragma: no cover
                                                    "debug", "Applied automatic fixes"))

        return sorted(set(issues), key=lambda x: x[0])
    except Exception as e:
        import traceback
        print("OOPS - That shouldn't happen - {}".format(args.files))
        traceback.print_exc()
    return []

def main():  # pragma: no cover
    args = arguments_post(parse_arguments())

    if args.print_rulefile:
        print_rulefile(args)
        sys.exit(0)

    issues = run(args)

    if args.output != sys.stderr:
        args.output = open(args.output, "w")
    args.output.write("\n".join([x[1] for x in issues]) + "\n")
    if args.output != sys.stderr:
        args.output.close()

    exit_code = len(issues) if not args.exit_zero else 0
    sys.exit(exit_code)

if __name__ == '__main__':
    main()  # pragma: no cover
