import argparse
import json
import multiprocessing as mp
import os
import re
from configparser import ConfigParser, NoOptionError, NoSectionError, ParsingError
from functools import partial
from typing import Dict, Iterable, List, Tuple, Union

from oelint_parser.cls_item import Item
from oelint_parser.cls_item import Comment
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule, load_rules
from oelint_adv.rule_base.rule_file_inlinesuppress_na import (
    FileNotApplicableInlineSuppression,
)
from oelint_adv.state import State
from oelint_adv.tweaks import Tweaks


class TypeSafeAppendAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None) -> None:
        if not isinstance(values, str):
            return  # pragma: no cover
        items = getattr(namespace, self.dest) or []
        items.extend(RegexRpl.split(r'\s+|\t+|\n+', values.strip('"').strip("'")))
        setattr(namespace, self.dest, items)


def deserialize_boolean_options(options: Dict) -> Dict[str, Union[str, bool]]:
    """Converts strings in `options` that are either 'True' or 'False' to their boolean
    representations.
    """
    for k, v in options.items():
        if isinstance(v, str):
            if v.strip() == 'False':
                options[k] = False
            elif v.strip() == 'True':
                options[k] = True

    return options


def parse_configfile() -> Dict:
    if os.environ.get('OELINT_SKIP_CONFIG', ''):
        return {}
    config = ConfigParser()
    for conffile in [os.environ.get('OELINT_CONFIG', '/does/not/exist'),
                     os.path.join(os.getcwd(), '.oelint.cfg'),
                     os.path.join(os.environ.get('HOME', '/does/not/exist'), '.oelint.cfg')]:
        try:
            if not os.path.exists(conffile):
                continue
            config.read(conffile)
            items = {k.replace('-', '_'): v for k, v in config.items('oelint')}
            items = deserialize_boolean_options(items)

            return items
        except (PermissionError, SystemError) as e:  # pragma: no cover
            print(f'Failed to load config file {conffile}. {e!r}')  # noqa: T201 - it's fine here; # pragma: no cover
        except (NoSectionError, NoOptionError, ParsingError) as e:
            print(f'Failed parsing config file {conffile}. {e!r}')  # noqa: T201 - it's here for a reason

    return {}


def group_files(files: Iterable[str]) -> List[List[str]]:
    # in case multiple bb files are passed at once we might need to group them to
    # avoid having multiple, potentially wrong hits of include files shared across
    # the bb files in the stash
    res = {}
    for f in files:
        _filename, _ext = os.path.splitext(f)
        if _ext not in ['.bb']:
            continue
        if '_' in os.path.basename(_filename):
            _filename_key = _filename
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
            if any(RegexRpl.match(_needle, x) for x in v):
                v.add(f)
                _match = True
        if not _match:
            _filename_key = os.path.basename(_filename).replace('%', '')
            if _filename_key not in res:  # pragma: no cover
                res[_filename_key] = set()
            res[_filename_key].add(f)

    # as sets are unordered, we convert them to sorted lists at this point
    # order is like the files have been passed via CLI
    for k, v in res.items():
        res[k] = sorted(v, key=lambda index: files.index(index))

    return res.values()


def group_run(group: List[str],
              quiet: bool,
              fix: bool,
              rules: List[Rule],
              state: State) -> List[Tuple[str, int, str]]:
    fixedfiles = []
    stash = Stash(quiet=quiet, **state.get_additional_stash_args())
    for f in group:
        try:
            stash.AddFile(f)
        except FileNotFoundError as e:  # pragma: no cover
            if not quiet:  # pragma: no cover
                print('Can\'t open/read: {e}'.format(e=e))  # noqa: T201 - it's fine here; # pragma: no cover

    stash.Finalize()

    inline_supp_map = {}
    for item in stash.GetItemsFor(classifier=Comment.CLASSIFIER):
        for line in item.get_items():
            m = re.match(
                r'^#\s+nooelint:\s+(?P<ids>[A-Za-z0-9\.,_ ]*)', line)
            if m:
                if item.Origin not in inline_supp_map:  # pragma: no cover
                    inline_supp_map[item.Origin] = {}
                inline_supp_map[item.Origin][item.InFileLine] = [
                    x.strip() for x in m.group('ids').split(',') if x]

    state.inline_suppressions = inline_supp_map

    _files = list(set(stash.GetRecipes() + stash.GetLoneAppends()))
    issues = []
    for _, f in enumerate(_files):
        for r in rules:
            if not r.OnAppend and f.endswith('.bbappend'):
                continue
            if r.OnlyAppend and not f.endswith('.bbappend'):
                continue
            if fix:
                fixedfiles += r.fix(f, stash)
            issues += r.check(f, stash)
    fixedfiles = list(set(fixedfiles))
    for f in fixedfiles:
        items: List[Item] = stash.GetItemsFor(filename=f)
        for file in {x.Origin for x in items}:
            if not state.nobackup:
                os.rename(file, file + '.bak')  # pragma: no cover
            with open(file, 'w') as o:
                o.write(''.join([x.RealRaw for x in sorted(items, key=lambda key: key.InFileLine) if x.Origin == file]))
                if not quiet:
                    print('{path}:{lvl}:{msg}'.format(path=os.path.abspath(file),  # noqa: T201 - it's fine here; # pragma: no cover
                          lvl='debug', msg='Applied automatic fixes'))

    if any(isinstance(x, FileNotApplicableInlineSuppression) for x in rules):
        for _file, _lineobj in inline_supp_map.items():
            for _line, _ids in _lineobj.items():
                for _id in _ids:
                    if not state.get_inline_suppression_seen(_file, _line, _id):
                        obj = FileNotApplicableInlineSuppression(state)
                        issues += obj.finding(_file, _line, override_msg=obj.Msg.format(id=_id))

    return issues


def flatten(list_: Iterable) -> List:
    if not isinstance(list_, list):
        return [list_]
    flat = []
    for sublist in list_:
        flat.extend(flatten(sublist))
    return flat


def create_lib_arguments(files: List[str],
                         suppressions: List[str] = None,
                         fix: bool = False,
                         nobackup: bool = False,
                         additional_rules: List[str] = None,
                         rulefile: str = None,
                         jobs: int = None,
                         color: bool = False,
                         quiet: bool = False,
                         noinfo: bool = False,
                         nowarn: bool = False,
                         hide: List[str] = None,
                         relpaths: bool = False,
                         messageformat: str = None,
                         constantmods: List[str] = None,
                         release: str = None) -> argparse.Namespace:
    """Create runtime arguments in library mode

    Args:
        files (List[str]): List of files to lint
        suppressions (List[str], optional): List of suppressions. Defaults to None.
        fix (bool, optional): Automatically fix fixable issues. Defaults to False.
        nobackup (bool, optional): No backup for fixed files. Defaults to False.
        additional_rules (List[str], optional): Path(s) to directories with additional rules. Defaults to None.
        rulefile (str, optional): Path to rulefile. Defaults to None.
        jobs (int, optional): Number of jobs. Defaults to None.
        color (bool, optional): Color output. Defaults to False.
        quiet (bool, optional): Quiet mode. Defaults to False.
        hide (List[str], optional): hide messages of specified severity. Defaults to None.
        noinfo (bool, optional): No info messages. Defaults to False. (legacy interface)
        nowarn (bool, optional): No warning messages. Defaults to False. (legacy interface)
        relpaths (bool, optional): Use relative paths in output. Defaults to False.
        messageformat (str, optional): Override message format. Defaults to None.
        constantmods (List[str], optional): Constant mods. Defaults to None.
        release (str, optional): Release to check against. Defaults to None.

    Returns:
        argparse.Namespace: runtime arguments
    """
    parser = argparse.ArgumentParser()
    parser.register('action', 'tsappend', TypeSafeAppendAction)
    parser.add_argument('--suppress', default=[])
    parser.add_argument('--fix', action='store_true', default=False)
    parser.add_argument('--nobackup', action='store_true', default=False)
    parser.add_argument('--addrules', nargs='+', default=[])
    parser.add_argument('--customrules', nargs='+', default=[])
    parser.add_argument('--rulefile', default=None)
    parser.add_argument('--quiet', action='store_true', default=False)
    parser.add_argument('--jobs', type=int, default=mp.cpu_count())
    parser.add_argument('--color', action='store_true', default=False)
    parser.add_argument('--hide', action='append', default=None,
                        choices=['info', 'warning', 'error'])
    parser.add_argument('--noinfo', action='store_true', default=False)
    parser.add_argument('--nowarn', action='store_true', default=False)
    parser.add_argument('--relpaths', action='store_true', default=False)
    parser.add_argument('--messageformat', default='{path}:{line}:{severity}:{id}:{msg}', type=str)
    parser.add_argument('--constantmods', default=[], nargs='+')
    parser.add_argument('--release', default=Tweaks.DEFAULT_RELEASE, choices=Tweaks._map.keys())
    # Override the defaults with the values from the config file
    parser.set_defaults(**parse_configfile())

    parser.add_argument('files', nargs='*')

    dummy_args = [y for y in [
        *['--suppress={x}' for x in (suppressions or ())],
        '--fix' if fix else '',
        '--nobackup' if nobackup else '',
        *['--addrules={x}' for x in (additional_rules or ())],
        '--rulefile={rulefile}' if rulefile else '',
        '--jobs={jobs}' if jobs else '',
        '--color' if color else '',
        '--quiet' if quiet else '',
        '--noinfo' if noinfo else '',
        '--nowarn' if nowarn else '',
        *['--hide={x}' for x in (hide or ())],
        '--relpaths' if relpaths else '',
        '--messageformat={messageformat}' if messageformat else '',
        *['--constantmods={x}' for x in (constantmods or ())],
        '--release={release}' if release else '',
        *files,
    ] if y != '']

    return arguments_post(parser.parse_args(dummy_args))


def arguments_post(args: argparse.Namespace) -> argparse.Namespace:  # noqa: C901 - complexity is still okay
    setattr(args, 'state', State())  # noqa: B010

    # Apply release specific tweaks
    args = Tweaks.tweak_args(args)

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
        'addrules',
        'constantmods',
        'customrules',
        'suppress',
        'hide',
    ]:
        try:
            if not isinstance(getattr(args, _option), list):
                setattr(args, _option, [x.strip() for x in (
                    getattr(args, _option) or '').split('\n') if x])
        except AttributeError:  # pragma: no cover
            pass  # pragma: no cover

    if args.files == [] and not args.print_rulefile:
        raise argparse.ArgumentTypeError('no input files')

    if args.rulefile:
        try:
            with open(args.rulefile) as i:
                args.state.rule_file = json.load(i)
        except (FileNotFoundError, json.JSONDecodeError):
            raise argparse.ArgumentTypeError(
                '\'rulefile\' is not a valid file')

    if args.hide:
        for severity in args.hide:
            args.state.hide[severity] = True

    if args.noinfo:
        args.state.hide['info'] = True

    if args.nowarn:
        args.state.hide['warning'] = True

    for mod in args.constantmods:
        if isinstance(mod, str):
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
        else:
            CONSTANTS.AddConstants(mod.get('+', {}))
            CONSTANTS.RemoveConstants(mod.get('-', {}))

    args.state.color = args.color
    args.state.nobackup = args.nobackup
    args.state.rel_path = args.relpaths
    args.state.suppression = args.suppress

    args.state.messageformat = args.messageformat

    return args


def run(args: argparse.Namespace) -> List[Tuple[Tuple[str, int], str]]:
    rules = load_rules(args, add_rules=args.addrules,
                       add_dirs=args.customrules)
    _loaded_ids = []
    _rule_file = args.state.get_rulefile()

    def rule_applicable(rule):
        if isinstance(rule, Rule):
            res = not _rule_file or any(x in _rule_file for x in rule.get_ids())  # pragma: no cover
            res &= rule.ID not in args.state.get_suppressions()
        else:
            res = not _rule_file or rule in _rule_file
            res &= rule not in args.state.get_suppressions()
        return res

    rules = [x for x in rules if rule_applicable(x)]

    for r in rules:
        _loaded_ids += [x for x in r.get_ids() if rule_applicable(x)]
    if not args.quiet:
        print('Loaded rules:\n\t{rules}'.format(  # noqa: T201 - it's here for a reason
            rules='\n\t'.join(sorted(_loaded_ids))))
    issues = []
    groups = group_files(args.files)
    if not any(groups):
        return []
    with mp.Pool(processes=min(args.jobs, len(groups))) as pool:
        try:
            issues = flatten(pool.map(partial(group_run, quiet=args.quiet, fix=args.fix,
                                              rules=rules, state=args.state), groups))
        finally:
            pool.close()
            pool.join()

    return sorted(set(issues), key=lambda x: x[0])
