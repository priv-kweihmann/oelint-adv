import argparse
import sys
from typing import List, Tuple


class OutputFormatStdOut():

    def __init__(self, args: argparse.Namespace, issues: List[Tuple[str, int, str]]) -> None:
        if args.output != sys.stderr:
            args.output = open(args.output, 'w')  # pragma: no cover
        args.output.write('\n'.join([x[1] for x in issues]))
        if issues:  # pragma: no cover
            args.output.write('\n')
        if args.output != sys.stderr:
            args.output.close()  # pragma: no cover


class OutputFormatJUnit():

    def __init__(self, args: argparse.Namespace, issues: List[Tuple[str, int, str]]) -> None:
        output = '<?xml version="1.0" encoding="UTF-8"?>\n'
        output += '<testsuites>\n'
        if not issues:
            output += '<testsuite id="oelint-adv" name="oelint-adv" tests="1" failures="0" errors="0" skipped="0">\n'
            output += '<testcase name="oelint.run.passed"/>\n'
        else:
            output += f'<testsuite id="oelint-adv" name="oelint-adv" tests="{len(issues)}" failures="{len(issues)}" errors="0" skipped="0">\n'
            for x in issues:
                _file, _line, _id = x[0]
                _msg = x[1]
                output += f'<testcase name="{_id}" file="{_file}" line="{_line}">\n'
                output += f'<failure message="{_id}" type="failure">\n'
                output += _msg
                output += '</failure>\n'
                output += '</testcase>\n'
        output += '</testsuite>\n'
        output += '</testsuites>\n'

        if args.output != sys.stderr:
            args.output = open(args.output, 'w')  # pragma: no cover
        args.output.write(output)
        if issues:
            args.output.write('\n')
        if args.output != sys.stderr:
            args.output.close()  # pragma: no cover


_OUTPUT_FORMATS = {
    'stdout': OutputFormatStdOut,
    'junit': OutputFormatJUnit,
}
