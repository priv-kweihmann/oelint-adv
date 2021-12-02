import argparse
import json
import os
import re
import sys
from configparser import ConfigParser
from configparser import NoOptionError
from configparser import NoSectionError
from configparser import ParsingError

from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import load_rules
from oelint_adv.color import set_colorize
from oelint_adv.rule_file import set_messageformat
from oelint_adv.rule_file import set_noinfo
from oelint_adv.rule_file import set_nowarn
from oelint_adv.rule_file import set_relpaths
from oelint_adv.rule_file import set_rulefile
from oelint_adv.rule_file import set_suppressions

sys.path.append(os.path.abspath(os.path.join(__file__, '..')))


class TypeSafeAppendAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        if isinstance(items, str):
            items = re.split(r'\s+|\t+|\n+', items)  # pragma: no cover
        items.append(values)  # pragma: no cover
        setattr(namespace, self.dest, items)  # pragma: no cover


def parse_configfile():
    config = ConfigParser()
    for conffile in [os.environ.get('OELINT_CONFIG', '/does/not/exist'),
                     os.path.join(os.getcwd(), '.oelint.cfg'),
                     os.path.join(os.environ.get('HOME', '/does/not/exist'), '.oelint.cfg')]:
        try:
            if not os.path.exists(conffile):
                continue
            config.read(conffile)
            return {k.replace('-', '_'): v for k, v in config.items('oelint')}
        except (PermissionError, SystemError) as e:  # pragma: no cover
            print(f'Failed to load config file {conffile}. {e!r}')  # noqa: T001 - it's fine here; # pragma: no cover
        except (NoSectionError, NoOptionError, ParsingError) as e:
            print(f'Failed parsing config file {conffile}. {e!r}')  # noqa: T001 - it's here for a reason
    return {}


def create_argparser():
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
                        help='Additional directories to parse for rulessets')
    parser.add_argument('--rulefile', default=None,
                        help='Rulefile')
    parser.add_argument('--constantfile', default=None, help='Constantfile')
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
    parser.add_argument('--noid', action='store_true', default=False,
                        help='Don\'t show the error-ID in the output')
    parser.add_argument('--messageformat', default='{path}:{line}:{severity}:{id}:{msg}',
                        type=str, help='Format of message output')
    parser.add_argument('--constantmods', default=[], nargs='+',
                        help='''
                             Modifications to the constant db.
                             prefix with:
                             + - to add to DB,
                             - - to remove from DB,
                             None - to override DB
                            ''')
    parser.add_argument('--print-rulefile', action='store_true', default=False,
                        help='Print loaded rules as a rulefile and exit')
    parser.add_argument('--exit-zero', action='store_true', default=False,
                        help='Always return a 0 (non-error) status code, even if lint errors are found')
    # Override the defaults with the values from the config file
    parser.set_defaults(**parse_configfile())

    parser.add_argument('files', nargs='*', help='File to parse')

    return parser


def parse_arguments():
    return create_argparser().parse_args()  # pragma: no cover


def arguments_post(args):  # noqa: C901 - complexity is still okay
    # Convert boolean symbols
    for _option in [
        'color',
        'exit_zero',
        'fix',
        'nobackup',
        'noinfo',
        'nowarn',
        'print_rulefile',
        'quiet',
        'relpaths',
    ]:
        try:
            setattr(args, _option, bool(getattr(args, _option)))
        except AttributeError:  # pragma: no cover
            pass  # pragma: no cover

    # Convert list symbols
    for _option in [
        'suppress',
        'constantmods',
    ]:
        try:
            if not isinstance(getattr(args, _option), list):
                setattr(args, _option, [x.strip() for x in (getattr(args, _option) or '').split('\n') if x])
        except AttributeError:  # pragma: no cover
            pass  # pragma: no cover

    if args.files == [] and not args.print_rulefile:
        raise argparse.ArgumentTypeError('no input files')

    if args.rulefile:
        try:
            with open(args.rulefile) as i:
                set_rulefile(json.load(i))
        except (FileNotFoundError, json.JSONDecodeError):
            raise argparse.ArgumentTypeError(
                '\'rulefile\' is not a valid file')

    if args.constantfile:
        try:
            with open(args.constantfile) as i:
                CONSTANTS.AddFromConstantFile(json.load(i))
        except (FileNotFoundError, json.JSONDecodeError):
            raise argparse.ArgumentTypeError(
                '\'constantfile\' is not a valid file')

    for mod in args.constantmods:
        try:
            with open(mod.lstrip('+-')) as _in:
                _cnt = json.load(_in)
            if mod.startswith('+'):
                CONSTANTS.AddConstants(_cnt)
            elif mod.startswith('-'):
                CONSTANTS.RemoveConstants(_cnt)
            else:
                CONSTANTS.OverrideConstants(_cnt)
        except (FileNotFoundError, json.JSONDecodeError):
            raise argparse.ArgumentTypeError(
                'mod file \'{file}\' is not a valid file'.format(file=mod))

    set_colorize(args.color)
    set_nowarn(args.nowarn)
    set_noinfo(args.noinfo)
    set_relpaths(args.relpaths)
    set_suppressions(args.suppress)
    if args.noid:
        # just strip id from message format if noid is requested
        args.messageformat = args.messageformat.replace('{id}', '')
        # strip any double : resulting from the previous operation
        args.messageformat = args.messageformat.replace('::', ':')
    set_messageformat(args.messageformat)
    return args


def group_files(files):
    # in case multiple bb files are passed at once we might need to group them to
    # avoid having multiple, potentially wrong hits of include files shared across
    # the bb files in the stash
    res = {}
    for f in files:
        _filename, _ext = os.path.splitext(f)
        if _ext not in ['.bb']:
            continue
        if '_' in os.path.basename(_filename):
            _filename_key = '_'.join(os.path.basename(
                _filename).split('_')[:-1]).replace('%', '')
        else:
            _filename_key = os.path.basename(_filename)
        if _filename_key not in res:  # pragma: no cover
            res[_filename_key] = set()
        res[_filename_key].add(f)

    # second round now for the bbappend files
    for f in files:
        _filename, _ext = os.path.splitext(f)
        if _ext not in ['.bbappend']:
            continue
        _match = False
        for _, v in res.items():
            _needle = '.*/' + os.path.basename(_filename).replace('%', '.*')
            if any(re.match(_needle, x) for x in v):
                v.add(f)
                _match = True
                break
        if not _match:
            _filename_key = '_'.join(os.path.basename(
                _filename).split('_')[:-1]).replace('%', '')
            if _filename_key not in res:  # pragma: no cover
                res[_filename_key] = set()
            res[_filename_key].add(f)

    # as sets are unordered, we convert them to sorted lists at this point
    # order is like the files have been passed via CLI
    for k, v in res.items():
        res[k] = sorted(v, key=lambda index: files.index(index))

    return res.values()


def print_rulefile(args):
    rules = load_rules(args, add_rules=args.addrules,
                       add_dirs=args.customrules)
    ruleset = {}
    for r in rules:
        ruleset.update(r.get_rulefile_entries())
    print(json.dumps(ruleset, indent=2))  # noqa: T001 - it's here for a reason


def run(args):
    try:
        rules = load_rules(args, add_rules=args.addrules,
                           add_dirs=args.customrules)
        _loaded_ids = []
        for r in rules:
            _loaded_ids += r.get_ids()
        if not args.quiet:
            print('Loaded rules:\n\t{rules}'.format(  # noqa: T001 - it's here for a reason
                rules='\n\t'.join(sorted(_loaded_ids))))
        issues = []
        fixedfiles = []
        groups = group_files(args.files)
        for group in groups:
            stash = Stash(args)
            for f in group:
                try:
                    stash.AddFile(f)
                except FileNotFoundError as e:  # pragma: no cover
                    if not args.quiet:  # pragma: no cover
                        print('Can\'t open/read: {e}'.format(e=e))  # noqa: T001 - it's fine here; # pragma: no cover

            stash.Finalize()

            _files = list(set(stash.GetRecipes() + stash.GetLoneAppends()))
            for _, f in enumerate(_files):
                for r in rules:
                    if not r.OnAppend and f.endswith('.bbappend'):
                        continue
                    if r.OnlyAppend and not f.endswith('.bbappend'):
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
                        os.rename(i, i + '.bak')  # pragma: no cover
                    with open(i, 'w') as o:
                        o.write(''.join([x.RealRaw for x in items]))
                        if not args.quiet:
                            print('{path}:{lvl}:{msg}'.format(path=os.path.abspath(i),  # noqa: T001 - it's fine here; # pragma: no cover
                                                    lvl='debug', msg='Applied automatic fixes'))

        return sorted(set(issues), key=lambda x: x[0])
    except Exception:
        import traceback

        # pragma: no cover
        print('OOPS - That shouldn\'t happen - {files}'.format(files=args.files))   # noqa: T001 - it's here for a reason
        # pragma: no cover
        traceback.print_exc()
    return []


def main():  # pragma: no cover
    args = arguments_post(parse_arguments())

    if args.print_rulefile:
        print_rulefile(args)
        sys.exit(0)

    issues = run(args)

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
