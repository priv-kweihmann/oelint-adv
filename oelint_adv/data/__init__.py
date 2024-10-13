import os

datapath = os.path.dirname(__file__)


def has_data_file(release: str) -> bool:
    return os.path.exists(os.path.join(datapath, f'{release}.json'))


def known_variable_mod(release: str) -> str:
    if has_data_file(release):
        return os.path.join(datapath, f'{release}.json')
    return ''
