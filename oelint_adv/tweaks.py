import argparse


class Tweaks:
    """Release specific tweaks"""

    DEFAULT_RELEASE = 'scarthgap'

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
        "mickledore": {"constantmods": {"-": {"variables": {"known": ["PACKAGEBUILDPKGD"]}}}},
        "nanbield": {"constantmods": {"-": {"variables": {"suggested": ["AUTHOR"]}}}},
        "scarthgap": {},
        "styhead": {"constantmods": {"+": {"variables": {"known": ["UNPACKDIR"]}}}},
        "walnascar": {},
        "latest": {},
    }

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

        setattr(args, '_release_range', _release_range)  # noqa: B010
        args.state.additional_stash_args = getattr(args, '_stash_args', {})
        return args
