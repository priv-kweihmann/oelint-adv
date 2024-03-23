import argparse
import json
import multiprocessing as mp
import os
import sys

# PYTHON_ARGCOMPLETE_OK
import argcomplete

from oelint_adv.cls_rule import load_rules
from oelint_adv.core import TypeSafeAppendAction, arguments_post, parse_configfile, run
from oelint_adv.tweaks import Tweaks
from oelint_adv.version import __version__

sys.path.append(os.path.abspath(os.path.join(__file__, '..')))


def _constantmod_completer(prefix, parsed_args, **kwargs):
    if prefix.startswith('+'):  # pragma: no cover
        return [f'+{x}' for x in argcomplete.FilesCompleter().__call__(prefix[1:], **kwargs)]  # pragma: no cover
    elif prefix.startswith('-'):  # pragma: no cover
        # doesn't seem to work with argcomplete, but maybe in this could be resolved
        # by the upstream implementation
        return [f'-{x}' for x in argcomplete.FilesCompleter().__call__(prefix[1:], **kwargs)]  # pragma: no cover
    return argcomplete.FilesCompleter().__call__(prefix, **kwargs) + ['+', '-']  # pragma: no cover


def create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='oelint-adv',
                                     description='Advanced OELint - Check bitbake recipes against OECore styleguide')
    parser.register('action', 'tsappend', TypeSafeAppendAction)
    parser.add_argument('--suppress', default=[],
                        action='tsappend', help='Rules to suppress')
    parser.add_argument('--output', default=sys.stderr,
                        help='Where to flush the findings (default: stderr)')
    parser.add_argument('--fix', action='store_true', default=False,
                        help='Automatically try to fix the issues')
    parser.add_argument('--nobackup', action='store_true', default=False,
                        help='Don\'t create backup file when auto fixing')
    parser.add_argument('--addrules', nargs='+', default=[],
                        help='Additional non-default rulessets to add')
    parser.add_argument('--customrules', nargs='+', default=[],
                        help='Additional directories to parse for rulessets').completer = argcomplete.DirectoriesCompleter
    parser.add_argument('--rulefile', default=None,
                        help='Rulefile')
    parser.add_argument('--jobs', type=int, default=mp.cpu_count(),
                        help='Number of jobs to run (default all cores)')
    parser.add_argument('--color', action='store_true', default=False,
                        help='Add color to the output based on the severity')
    parser.add_argument('--quiet', action='store_true', default=False,
                        help='Print findings only')
    parser.add_argument('--noinfo', action='store_true', default=False,
                        help='Don\'t print information level findings')
    parser.add_argument('--nowarn', action='store_true', default=False,
                        help='Don\'t print warning level findings')
    parser.add_argument('--relpaths', action='store_true', default=False,
                        help='Show relative paths instead of absolute paths in results')
    parser.add_argument('--messageformat', default='{path}:{line}:{severity}:{id}:{msg}',
                        type=str, help='Format of message output')
    parser.add_argument('--constantmods', default=[], nargs='+',
                        help='''
                             Modifications to the constant db.
                             prefix with:
                             + - to add to DB,
                             - - to remove from DB,
                             None - to override DB
                            ''').completer = _constantmod_completer
    parser.add_argument('--print-rulefile', action='store_true', default=False,
                        help='Print loaded rules as a rulefile and exit')
    parser.add_argument('--exit-zero', action='store_true', default=False,
                        help='Always return a 0 (non-error) status code, even if lint errors are found')
    parser.add_argument('--release', default=Tweaks.DEFAULT_RELEASE, choices=Tweaks._map.keys(),
                        help='Run against a specific Yocto release')
    # Override the defaults with the values from the config file
    parser.set_defaults(**parse_configfile())

    parser.add_argument(
        'files', nargs='*', help='File to parse').completer = argcomplete.FilesCompleter(allowednames=('bb', 'bbappend', 'bbclass', 'conf'))
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s {__version__}')

    return parser


def parse_arguments() -> argparse.Namespace:
    parser = create_argparser()  # pragma: no cover
    argcomplete.autocomplete(parser)  # pragma: no cover
    return parser.parse_args()  # pragma: no cover


def print_rulefile(args: argparse.Namespace) -> None:
    rules = load_rules(args, add_rules=args.addrules,
                       add_dirs=args.customrules)
    ruleset = {}
    for r in rules:
        ruleset.update(r.get_rulefile_entries())
    print(json.dumps(ruleset, indent=2))  # noqa: T201 - it's here for a reason


def main() -> int:  # pragma: no cover
    args = arguments_post(parse_arguments())

    if args.print_rulefile:
        print_rulefile(args)
        sys.exit(0)

    try:
        issues = run(args)
    except Exception as e:  # pragma: no cover - that shouldn't be covered anyway
        import traceback
        print('OOPS - That shouldn\'t happen: {e} - {files}'.format(e=e, files=args.files))
        traceback.print_exc()
        sys.exit(-1)

    if args.output != sys.stderr:
        args.output = open(args.output, 'w')
    args.output.write('\n'.join([x[1] for x in issues]))
    if issues:
        args.output.write('\n')
    if args.output != sys.stderr:
        args.output.close()

    exit_code = len(issues) if not args.exit_zero else 0
    sys.exit(exit_code)


if __name__ == '__main__':
    main()  # pragma: no cover
