from oelint_adv.cls_stash import Stash
from oelint_adv.cls_rule import load_rules
import os
import sys
import argparse
import glob

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
    parser.add_argument("files", nargs='+', help="File to parse")
    return parser


if __name__ == '__main__':
    args = create_argparser().parse_args()
    rules = [x for x in load_rules() if str(x) not in args.suppress]
    print("Loaded rules: {}".format(",".join(sorted([str(x) for x in rules]))))
    stash = Stash()
    issues = []
    fixedfiles = []
    for f in args.files:
        try:
            stash.AddFile(f)
        except FileNotFoundError:
            print("Can't open/read {}".format(f))

    for f in stash.GetRecipes():
        for r in rules:
            if args.fix:
                fixedfiles += r.fix(f, stash)
            issues += r.check(f, stash)
    fixedfiles = list(set(fixedfiles))
    for f in fixedfiles:
        items = sorted(stash.GetItemsFor(filename=f), key = lambda x: x.Line)
        if not args.nobackup:
            os.rename(f, f + ".bak")
        with open(f, "w") as o:
            o.write("".join([x.Raw for x in items]))
            print("{}:{}:{}".format(os.path.abspath(f), "debug", "Applied automatic fixes"))

    issues = list(set(issues))
    if args.output != sys.stderr:
        args.output = open(args.output, "w")
    args.output.write("\n".join(sorted(issues)) + "\n")
    sys.exit(len(issues))
