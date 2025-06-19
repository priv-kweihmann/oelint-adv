import argparse
import copy
import fnmatch
import itertools
import json
import multiprocessing as mp
import os
import re
from configparser import ConfigParser, NoOptionError, NoSectionError, ParsingError
from functools import partial
from typing import Dict, Iterable, List, Tuple, Union

from oelint_parser.cls_item import Comment, Item
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.caches import Caches, __default_cache_dir
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
        if not isinstance(items, list):
            items = [x.strip() for x in items.split() if x.strip()]
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


def group_files(files: Iterable[str], mode: str) -> List[Tuple[List[str], List[str], Dict]]:
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
            _needle = '^.*/' + re.escape(os.path.basename(_filename)).replace('%', '.*') + '.bb$'
            if any(RegexRpl.match(_needle, x, re.MULTILINE) for x in v):
                v.add(f)
                _match = True
        if not _match:
            _filename_key = os.path.basename(_filename).replace('%', '')
            if _filename_key not in res:  # pragma: no cover
                res[_filename_key] = set()
            res[_filename_key].add(f)

    # third round for lone bbclasses
    for f in files:
        _filename, _ext = os.path.splitext(f)
        if _ext not in ['.bbclass']:
            continue
        if '_' in os.path.basename(_filename):
            _filename_key = _filename
        else:
            _filename_key = os.path.basename(_filename)
        if _filename_key not in res:  # pragma: no cover
            res[_filename_key] = set()
        res[_filename_key].add(f)

    # layer.confs
    _conf_layer = sorted([x for x in files if os.path.basename(x) == 'layer.conf'], key=lambda index: files.index(index))

    _product_matrix = []
    _conf_machine = []
    _conf_distro = []

    # as sets are unordered, we convert them to sorted lists at this point
    # order is like the files have been passed via CLI
    for k, v in res.items():
        res[k] = sorted(v, key=lambda index: files.index(index))

    if mode in ['all']:
        # machine.confs
        _conf_machine = [x for x in files if fnmatch.fnmatch(os.path.abspath(x), '*/machine/*.conf')]
        if any(_conf_machine):
            _product_matrix.append(_conf_machine)

        # distro.confs
        _conf_distro = [x for x in files if fnmatch.fnmatch(os.path.abspath(x), '*/distro/*.conf')]
        if any(_conf_distro):
            _product_matrix.append(_conf_distro)

        # pos and neg branch expansion
        _product_matrix.append([True, False])
    else:
        _product_matrix.append([False])

    group_res = []

    for fg in res.values():
        _fl = sorted(fg, key=lambda index: files.index(index))
        for element in itertools.product(*_product_matrix):
            _branch_expansion = element[-1]
            _matrix_keys = [f'branch:{"false" if _branch_expansion else "true"}']
            if len(element) > 1:
                _files = _conf_layer + list(element[:-1]) + _fl

                _machine_id = [x for x in _files if x in _conf_machine]
                _distro_id = [x for x in _files if x in _conf_distro]

                if any(_machine_id):
                    _matrix_keys.append(os.path.basename(_machine_id[0]))

                if any(_distro_id):
                    _matrix_keys.append(os.path.basename(_distro_id[0]))
            else:
                _files = _conf_layer + _fl
            group_res.append((_files, frozenset(_matrix_keys), {'negative_inline': _branch_expansion}))

    if _conf_layer:
        if mode in ['all']:
            group_res.append((_conf_layer, frozenset(['branch=true']), {'negative_inline': True}))
        group_res.append((_conf_layer, frozenset(['branch=false']), {'negative_inline': False}))

    for m in _conf_machine:
        # mode == all is implicit at this stage
        group_res.append(([m], frozenset(['branch=true']), {'negative_inline': True}))
        group_res.append(([m], frozenset(['branch=false']), {'negative_inline': False}))

    for d in _conf_distro:
        # mode == all is implicit at this stage
        group_res.append(([d], frozenset(['branch=true']), {'negative_inline': True}))
        group_res.append(([d], frozenset(['branch=false']), {'negative_inline': False}))

    return group_res


def group_run(group: List[Tuple],
              quiet: bool,
              fix: bool,
              rules: List[Rule],
              state: State) -> List[Tuple[str, int, str]]:
    fixedfiles = []
    group_files, matrix, stash_params = group
    stash = Stash(quiet=quiet, **state.get_additional_stash_args(), **stash_params)

    for f in group_files:
        try:
            stash.AddFile(f)
        except FileNotFoundError as e:  # pragma: no cover
            if not quiet:  # pragma: no cover
                print('Can\'t open/read: {e}'.format(e=e))  # noqa: T201 - it's fine here; # pragma: no cover

    stash.Finalize()

    cached_res = state._caches.GetFromCache([x.ID for x in rules], stash.FingerPrint)
    if cached_res is not None:
        return cached_res

    inline_supp_map = {}
    for item in stash.GetItemsFor(classifier=Comment.CLASSIFIER):
        for line in item.get_items():
            m = re.match(
                r'^#\s+nooelint:\s+(?P<ids>[A-Za-z0-9\.,_\s-]*)', line)
            if m:
                if item.Origin not in inline_supp_map:  # pragma: no cover
                    inline_supp_map[item.Origin] = {}
                inline_supp_map[item.Origin][item.InFileLine] = [
                    x.strip() for x in re.split(r',|\s+', m.group('ids')) if x]

    state.inline_suppressions = {**state.inline_suppressions, **inline_supp_map}

    rules = [copy.deepcopy(x) for x in rules]
    for rule in rules:
        rule.set_state(state)
        rule.set_product_matrix(matrix)
        rule.set_rungroup(group_files)

    _files = list(set(stash.GetRecipes() + stash.GetLoneAppends() + stash.GetConfFiles() + stash.GetBBClasses()))
    issues = []
    for _, f in enumerate(_files):
        _classification = Rule.classify_file(f)
        for r in rules:
            if not r.should_run(_classification):
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
        known_ids = list(itertools.chain(*[x.get_ids() for x in rules]))
        for _file, _lineobj in inline_supp_map.items():
            for _line, _ids in _lineobj.items():
                for _id in _ids:
                    if not state.get_inline_suppression_seen(_file, _line, _id):
                        if _id not in known_ids:
                            continue
                        obj = FileNotApplicableInlineSuppression(state)
                        issues += obj.finding(_file, _line, override_msg=obj.Msg.format(id=_id))

    state._caches.SaveToCache([x.ID for x in rules], stash.FingerPrint, issues)

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
                         release: str = None,
                         mode: str = 'fast',
                         cached: bool = False,
                         cachedir: str = __default_cache_dir,
                         extra_layer: List[str] = None) -> argparse.Namespace:
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
        mode (str, optional): Level of testing. Defaults to fast.
        cached (bool, optional): Use caching
        cachedir (str, optional): Path to cache directory,
        extra_layer (List[str], optional): Extra 3rd party layer to load data for

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
    parser.add_argument('--release', default=Tweaks.DEFAULT_RELEASE, choices=Tweaks.releases())
    parser.add_argument('--mode', default='fast', choices=['fast', 'all'])
    parser.add_argument('--cached', action='store_true', help='Use caches')
    parser.add_argument('--cachedir', default=os.environ.get('OELINT_CACHE_DIR', __default_cache_dir),
                        help=f'Cache directory (default {__default_cache_dir})')
    parser.add_argument('--clear-caches', action='store_true', help='Clear cache directory and exit')
    parser.add_argument('--extra-layer', nargs='*', action='extend',
                        default=['core'], help='Layer names of 3rd party layers to use')
    # Override the defaults with the values from the config file
    parser.set_defaults(**parse_configfile())

    parser.add_argument('files', nargs='*')

    dummy_args = [y for y in [
        *[f'--suppress={x}' for x in (suppressions or ())],
        '--fix' if fix else '',
        '--nobackup' if nobackup else '',
        *[f'--addrules={x}' for x in (additional_rules or ())],
        f'--rulefile={rulefile}' if rulefile else '',
        f'--jobs={jobs}' if jobs else '',
        '--color' if color else '',
        '--quiet' if quiet else '',
        '--noinfo' if noinfo else '',
        '--nowarn' if nowarn else '',
        *[f'--hide={x}' for x in (hide or ())],
        '--relpaths' if relpaths else '',
        f'--messageformat={messageformat}' if messageformat else '',
        *[f'--constantmods={x}' for x in (constantmods or ())],
        f'--release={release}' if release else '',
        f'--mode={mode}',
        '--cached' if cached else '',
        f'--cachedir={cachedir}',
        *[f'--extra-layer={x}' for x in (extra_layer or ())],
        * files,
    ] if y != '']

    return arguments_post(parser.parse_args(dummy_args))


def arguments_post(args: argparse.Namespace) -> argparse.Namespace:  # noqa: C901 - complexity is still okay
    setattr(args, 'state', State())  # noqa: B010

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

    # Apply release specific tweaks
    args = Tweaks.tweak_args(args)

    if args.files == [] and not args.print_rulefile and not args.clear_caches:
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

    args.state._caches = Caches(args)

    for mod in args.constantmods:
        if isinstance(mod, str):
            try:
                with open(mod.lstrip('+-')) as _in:
                    _cnt = json.load(_in)
                if mod.startswith('+'):
                    CONSTANTS.AddConstants(_cnt)
                    args.state._caches.AddToFingerPrint(f'+{_cnt}')
                elif mod.startswith('-'):
                    CONSTANTS.RemoveConstants(_cnt)
                    args.state._caches.AddToFingerPrint(f'-{_cnt}')
                else:
                    CONSTANTS.OverrideConstants(_cnt)
                    args.state._caches.AddToFingerPrint(str(_cnt))
            except (FileNotFoundError, json.JSONDecodeError):
                raise argparse.ArgumentTypeError(
                    'mod file \'{file}\' is not a valid file'.format(file=mod))
        else:
            CONSTANTS.AddConstants(mod.get('+', {}))
            CONSTANTS.RemoveConstants(mod.get('-', {}))
            args.state._caches.AddToFingerPrint(f'mod{mod.get("+", {})}')
            args.state._caches.AddToFingerPrint(f'mod{mod.get("-", {})}')

    args.state.color = args.color
    args.state.nobackup = args.nobackup
    args.state.rel_path = args.relpaths
    args.state.suppression = args.suppress

    args.state.messageformat = args.messageformat

    if args.fix and args.jobs > 1:
        args.jobs = 1
        print('WARNING: --fix should only be run in single job mode (--jobs=1) - downgrading to 1 job')  # noqa: T201

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
            res &= (rule.get_severity() in ['info', 'warning', 'error']) or any(
                rule.get_severity(x) in ['info', 'warning', 'error'] for x in rule.Appendix)
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
    groups = group_files(args.files, args.mode)
    if not any(groups):
        return []
    # Starting with python 3.14 the default way of starting the mp Pool
    # will be 'forkserver' - see https://docs.python.org/3.14/library/multiprocessing.html#contexts-and-start-methods
    # But in our setup we will need to share e.g. the CONSTANTS object into
    # the checks running in the Pool
    # Hence, we enforce fork
    ctx = mp.get_context('fork')
    with ctx.Pool(processes=min(args.jobs, len(groups))) as pool:
        try:
            issues = flatten(pool.map(partial(group_run, quiet=args.quiet, fix=args.fix,
                                              rules=rules, state=args.state), groups))
        finally:
            pool.close()
            pool.join()

    # deduplicate matrix
    def deduplicate(input_list):
        seen = []
        result = set()
        for item in input_list:
            needle = (item[0], item[2])
            if needle not in seen:
                seen.append(needle)
                matrix_str = f' [{",".join(sorted(item[1]))}]' if item[1] else ''
                result.add((item[0], f'{item[2]}{matrix_str}'))
        return result

    issues = sorted(deduplicate(issues), key=lambda x: x[0])

    return issues
