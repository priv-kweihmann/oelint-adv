import os
import json

from typing import List
from oelint_parser.cls_stash import Stash
datapath = os.path.dirname(__file__)


def known_variable_mod(release: str, layer: str) -> str:
    _file = os.path.join(datapath, release, f'{layer}.json')
    if os.path.exists(_file):
        return _file
    return ''


def layer_var_mods(files: str, release: str, external_layers: List[str]) -> List[str]:
    res = []
    imports = external_layers
    _specific = f'oelint.constants.{release}.json'
    _default = 'oelint.constants.json'
    _needles = {Stash(quiet=True).GetLayerRoot(x) for x in files}

    def get_imports(_file):
        with open(_file) as i:
            try:
                return json.load(i).get('$imports', [])
            except json.JSONDecodeError:  # pragma: no cover
                return []  # pragma: no cover

    for path in _needles:
        if not path:
            continue
        if os.path.exists(os.path.join(path, _specific)):
            _new_file = os.path.join(path, _specific)
            imports.extend(get_imports(_new_file))
            res.append(f'+{_new_file}')
        elif os.path.exists(os.path.join(path, _default)):
            _new_file = os.path.join(path, _default)
            imports.extend(get_imports(_new_file))
            res.append(f'+{_new_file}')
    return (res, imports)
