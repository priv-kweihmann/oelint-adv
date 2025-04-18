import argparse
import os
from typing import List

from oelint_data import known_variable_mod, layer_var_mods


class Tweaks:
    """Release specific tweaks"""

    standard_data_path = os.path.join(os.path.dirname(__file__), 'data', 'oelint.json')

    DEFAULT_RELEASE = 'walnascar'
    DEVELOPMENT_RELEASE = 'whinlatter'

    _map = {
        "inky": {},
        "clyde": {},
        "blinky": {},
        "pinky": {},
        "purple": {},
        "green": {},
        "laverne": {},
        "bernard": {},
        "edison": {},
        "denzil": {},
        "danny": {},
        "dylan": {},
        "dora": {},
        "daisy": {},
        "dizzy": {},
        "fido": {},
        "jethro": {},
        "krogoth": {},
        "morty": {},
        "pyro": {},
        "rocko": {},
        "sumo": {},
        "thud": {},
        "warrior": {},
        "zeus": {},
        "dunfell": {},
        "gatesgarth": {},
        "hardknott": {},
        "honister": {},
        "kirkstone": {"_stash_args": {"new_style_override_syntax": True}},
        "langdale": {},
        "mickledore": {},
        "nanbield": {"constantmods": {"-": {"variables": {"suggested": ["AUTHOR"]}}}},
        "scarthgap": {},
        "styhead": {},
        "walnascar": {},
        "whinlatter": {},
    }

    @staticmethod
    def releases() -> List[str]:
        return sorted(list(Tweaks._map.keys()) + ['latest'])

    @staticmethod
    def tweak_args(args: argparse.Namespace) -> argparse.Namespace:
        """Tweak the passed arguments for specific releases

        Args:
            args (argparse.Namespace): arguments from main

        Returns:
            argparse.Namespace: tweaked arguments
        """
        def recursive_merge(obj_a: dict, obj_b: dict) -> dict:
            if isinstance(obj_b, (list, str, bool)):
                return obj_b
            for k, v in obj_b.items():
                if obj_a.get(k, None) is None:  # pragma: no cover
                    obj_a[k] = {}
                if isinstance(obj_a[k], list):
                    obj_a[k] += recursive_merge(obj_a[k], v)  # pragma: no cover
                else:
                    obj_a[k] = recursive_merge(obj_a[k], v)
            return obj_a

        _tweaked_options = {}
        _release_range = []

        # override the latest alias
        if args.release == 'latest':
            args.release = Tweaks.DEVELOPMENT_RELEASE

        for k, v in Tweaks._map.items():   # pragma: no cover
            _tweaked_options = recursive_merge(_tweaked_options, v)
            _release_range.append(k)
            if k == args.release:
                break

        for k, v in _tweaked_options.items():
            item = getattr(args, k, None)
            if item is not None:
                if isinstance(item, list):   # pragma: no cover
                    item.append(v)
            else:
                setattr(args, k, v)

        # release known var constantmod
        modlist = [Tweaks.standard_data_path]
        release_mod = known_variable_mod(args.release, 'core')
        fallback_release_mod = known_variable_mod('fallback', 'core')
        if release_mod:
            modlist += [release_mod]
        else:
            if not args.print_rulefile:
                print('Using legacy dataset, accuracy of checks can not be guaranteed!')  # noqa: T201, pragma: no cover
            modlist += [fallback_release_mod]

        mods, third_party = layer_var_mods(args.files, args.release, args.extra_layer)
        modlist += mods
        for layer in third_party:
            mod = known_variable_mod(args.release, layer)
            if mod:
                modlist += [f'+{mod}']
        args.constantmods[0:0] = modlist

        setattr(args, '_release_range', _release_range)  # noqa: B010
        args.state.additional_stash_args = getattr(args, '_stash_args', {})
        return args
