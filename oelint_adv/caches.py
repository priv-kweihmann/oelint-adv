import argparse
import hashlib
import os
import pickle  # noqa: S403
import shutil
from typing import Any, List, Tuple, Union

__default_cache_dir = os.path.join(os.environ.get('HOME'), '.oelint/caches')


class Caches():

    def __init__(self, args: argparse.Namespace) -> None:
        self.__directory = args.cachedir
        self.__enabled = args.cached
        self.__quiet = args.quiet
        self.__arg_fingerprint = self.__calculate_args_fingerprint(args)

        if self.__enabled:
            os.makedirs(self.__directory, exist_ok=True)

    @property
    def FingerPrint(self):
        return self.__arg_fingerprint

    def __calculate_args_fingerprint(self, args: argparse.Namespace) -> object:
        _hash = hashlib.sha1(usedforsecurity=False)
        for item in [
                # list all hashing relevant arguments
                args.suppress,
                args.relpaths,
                args.state.hide,
                args.release,
                args.color,
        ]:
            _hash.update(f'{item}'.encode())
        return _hash.hexdigest()

    def AddToFingerPrint(self, input_: Union[str, bytes]) -> None:
        _hash = hashlib.sha1(self.__arg_fingerprint.encode(), usedforsecurity=False)  # noqa: DUO130
        if isinstance(input_, str):
            input_ = input_.encode()
        _hash.update(input_)
        self.__arg_fingerprint = _hash.hexdigest()

    def ClearCaches(self) -> None:
        shutil.rmtree(self.__directory, ignore_errors=True)

    def GetFromCache(self, rule_ids: List[str], stash_fingerprint: str) -> Union[None, Tuple[Tuple[str, int], List[str], str]]:
        if not self.__enabled:
            return None
        _hash = hashlib.sha1(f'{self.__arg_fingerprint}{rule_ids}{stash_fingerprint}'.encode(), usedforsecurity=False)  # noqa: DUO130
        _hash_path = os.path.join(self.__directory, _hash.hexdigest())
        try:
            with open(_hash_path, 'rb') as i:  # pragma: no cover
                if not self.__quiet:
                    print(f'Using cached item {_hash_path}')
                return pickle.load(i)  # noqa: DUO103, S301
        except (pickle.PickleError, FileNotFoundError):
            return None

    def SaveToCache(self, rule_ids: List[str], stash_fingerprint: str, content: Any) -> None:
        if not self.__enabled:
            return
        _hash = hashlib.sha1(f'{self.__arg_fingerprint}{rule_ids}{stash_fingerprint}'.encode(), usedforsecurity=False)  # noqa: DUO130
        _hash_path = os.path.join(self.__directory, _hash.hexdigest())
        try:
            with open(_hash_path, 'wb') as o:
                return pickle.dump(content, o, protocol=0)
        except (pickle.PicklingError, FileNotFoundError):  # pragma: no cover
            pass  # pragma: no cover
