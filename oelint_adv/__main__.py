import os
import argparse
import glob
import sys

try:
    from .cls_rule import load_rules
    from .cls_stash import Stash
except (SystemError, ImportError):
    from cls_rule import load_rules
    from cls_stash import Stash

def create_argparser():
    parser = argparse.ArgumentParser(
        description='Advanced OELint - Check bitbake recipes against OECore styleguide')
    parser.add_argument("--suppress", default=[], action="append", help="Rules to suppress")
    parser.add_argument("--output", default=sys.stderr, help="Where to flush the findings (default: stderr)")
    parser.add_argument("files", nargs='+', help="File to parse")
    return parser

if __name__ == '__main__':
    args = create_argparser().parse_args()
    rules = [x for x in load_rules() if str(x) not in args.suppress] 
    print("Loaded rules: {}".format(",".join(sorted([str(x) for x in rules]))))
    stash = Stash()
    issues = []
    for f in args.files:
        try:
            stash.AddFile(f)
        except FileNotFoundError:
            print("Can't open/read {}".format(f))

    for f in stash.GetRecipes():
        for r in rules:
            issues += r.check(f, stash)
    issues = list(set(issues))
    if args.output != sys.stderr:
        args.output = open(args.output, "w")
    args.output.write("\n".join(sorted(issues)) + "\n")
    sys.exit(len(issues))