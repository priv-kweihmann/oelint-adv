#!/usr/bin/env python3
import json
import os
import subprocess  # noqa: S404

TEMPLATE_FILE = os.path.join(os.path.dirname(__file__), 'docs/template.md')
WIKI_PATH = os.path.join(os.path.dirname(__file__), 'docs/wiki')


def create_templates(map_: dict):
    for k, v in map_.items():
        if os.path.exists(os.path.join(WIKI_PATH, f'{k}.md')):
            continue

        if any(k.startswith(x) for x in [
            'oelint.append.protvars.',
            'oelint.task.order.',
            'oelint.var.inherit.',
            'oelint.var.inheritdevtool.',
            'oelint.var.mandatoryvar.',
            'oelint.var.order.',
            'oelint.var.suggestedvar.',
            'oelint.vars.bbvars.',
            'oelint.vars.filessetting.',
            'oelint.vars.pathhardcode.',
            'oelint.vars.pkgspecific.',
        ]):
            continue

        rpl_map = {
            '%title%': k,
            '%severity%': v,
        }

        cnt = ''
        with open(TEMPLATE_FILE) as i:
            cnt = i.read()

        with open(os.path.join(WIKI_PATH, f'{k}.md'), 'w') as o:
            for rk, rv in rpl_map.items():
                cnt = cnt.replace(rk, rv)
            o.write(cnt)


def main():
    try:
        create_templates(json.loads(subprocess.check_output(  # noqa: S607, S603
            ['python3', '-m', 'oelint_adv', '--print-rulefile', '--release=latest'], universal_newlines=True)))
    except subprocess.CalledProcessError:
        pass


if __name__ == '__main__':
    main()  # pragma: no cover
