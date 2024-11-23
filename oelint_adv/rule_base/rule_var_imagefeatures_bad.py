from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class ImageFeaturesBad(Rule):
    def __init__(self) -> None:
        self._map = {
            'allow-empty-password': ('warning', 'that is a security risk. Users can have accounts without password protection'),
            'allow-root-login': ('info', 'that is a security risk. Root can login into the system'),
            'dbg-pkgs': ('info', 'that exposes sensitive information. Use debuginfod instead'),
            'debug-tweaks': ('warning', 'that is a security risk. Allows limitless access without authentication'),
            'dev-pkgs': ('info', 'that is not recommended, as it bloats the image. Do not use in production'),
            'eclipse-debug': ('info', 'installs debugging tools that could expose sensitive information. Do not use in production'),
            'empty-root-password': ('warning', 'that is a security risk. Anyone can authenticate as root over serial without a password'),
            'post-install-logging': ('info', 'that could expose sensitive information. Not recommended for production'),
            'ptest-pkgs': ('info', 'that bloats the image. Never use in production'),
            'serial-autologin-root': ('warning', 'that is a security risk. Automatically logs in a root'),
            'staticdev-pkgs': ('info', 'that is not recommended, as it bloats the image. Do not use in production'),
            'tools-debug': ('info', 'installs debugging tools that could expose sensitive information. Do not use in production'),
        }
        super().__init__(id='oelint.var.badimagefeature',
                         severity='warning',
                         message='{var} contains \'{feature}\', {reason}',
                         appendix=list(self._map.keys()))

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for item in stash.GetItemsFor(filename=_file,
                                      classifier=Variable.CLASSIFIER,
                                      attribute=Variable.ATTR_VAR,
                                      attributeValue=("IMAGE_FEATURES", "EXTRA_IMAGE_FEATURES")):
            if 'remove' in item.SubItems:
                continue
            items = item.get_items()
            for k, v in self._map.items():
                if k in items:
                    severity, reason = v
                    res += self.finding(item.Origin, item.InFileLine,
                                        self.Msg.format(var=item.VarName, feature=k, reason=reason),
                                        appendix=k,
                                        severity_override=severity)
        return res
