import argparse
import os
import sys
import json

from oelint_adv.cls_rule import load_rules
from oelint_adv.cls_stash import Stash
from oelint_adv.color import set_color
from oelint_adv.rule_file import set_rulefile, set_constantfile, set_nowarn, set_noinfo

sys.path.append(os.path.abspath(os.path.join(__file__, "..")))


def create_argparser():
    parser = argparse.ArgumentParser(
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
    parser.add_argument("files", nargs='+', help="File to parse")

    args = parser.parse_args()

    if args.rulefile:
        try:
            with open(args.rulefile) as i:
                set_rulefile(json.load(i))
        except (FileNotFoundError, json.JSONDecodeError):
            raise argparse.ArgumentTypeError("'rulefile' is not a valid file")

    if args.constantfile:
        try:
            with open(args.constantfile) as i:
                set_constantfile(json.load(i))
        except (FileNotFoundError, json.JSONDecodeError):
            raise argparse.ArgumentTypeError(
                "'constantfile' is not a valid file")

    if args.color:
        set_color(True)
    if args.nowarn:
        set_nowarn(True)
    if args.noinfo:
        set_noinfo(True)
    return args


def main():
    args = create_argparser()
    rules = [x for x in load_rules(args,
        add_rules=args.addrules, add_dirs=args.customrules)]
    # filter out suppressions
    rules = [x for x in rules if not any(y in args.suppress for y in x.GetIDs())]
    _loadedIDs = []
    for r in rules:
        _loadedIDs += r.GetIDs()
    if not args.quiet:
        print("Loaded rules:\n\t{}".format("\n\t".join(sorted(_loadedIDs))))
    stash = Stash(args)
    issues = []
    fixedfiles = []
    for f in args.files:
        try:
            stash.AddFile(f)
        except FileNotFoundError as e:
            if not args.quiet:
                print("Can't open/read: {}".format(e))

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
        if not args.quiet:
            print("{}/{} files checked".format(index, len(_files)))
    fixedfiles = list(set(fixedfiles))
    for f in fixedfiles:
        _items = [f] + stash.GetLinksForFile(f)
        for i in _items:
            items = stash.GetItemsFor(filename=i, nolink=True)
            if not args.nobackup:
                os.rename(i, i + ".bak")
            with open(i, "w") as o:
                o.write("".join([x.Raw for x in items]))
                if not args.quiet:
                    print("{}:{}:{}".format(os.path.abspath(i),
                                            "debug", "Applied automatic fixes"))

    issues = sorted(set(issues), key=lambda x: x[0])

    if args.output != sys.stderr:
        args.output = open(args.output, "w")
    args.output.write("\n".join([x[1] for x in issues]) + "\n")
    if args.output != sys.stderr:
        args.output.close()
    sys.exit(len(issues))


if __name__ == '__main__':
    main()
