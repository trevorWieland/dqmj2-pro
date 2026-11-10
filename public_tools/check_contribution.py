"""Check changed authored files against the contribution rules.

Authored comments are allowed and encouraged, so the rules are deliberately
small: a 500-physical-line limit on formatted authored files. Run
``--selftest`` to exercise the rule functions on in-memory samples without a
git base, or ``--base <sha>`` to check the files changed since that revision.
"""

import argparse
import subprocess
from pathlib import Path


LINE_LIMIT = 500

SAMPLE_PASS = '''\
// Line comments explain mechanism and are allowed, not rejected.
/* Block comments explain intent and are allowed too. */
#include <stdint.h>

static int32_t clamp_to_range(int32_t value, int32_t minimum, int32_t maximum)
{
    if (value < minimum) {
        return minimum;
    }
    if (value > maximum) {
        return maximum;
    }
    return value;
}
'''

SAMPLE_FAIL = '\n'.join('int authored_line_%d;' % index for index in range(LINE_LIMIT + 1)) + '\n'


def check_text(text):
    """Return rule failures for authored text, independent of any file."""
    failures = []
    if len(text.splitlines()) > LINE_LIMIT:
        failures.append('more than 500 physical lines')
    return failures


def check(path):
    """Return rule failures for one authored file."""
    return check_text(path.read_text(encoding='utf-8-sig'))


def selftest():
    """Run the rules on two in-memory samples: one must pass, one must fail."""
    accepted = check_text(SAMPLE_PASS)
    rejected = check_text(SAMPLE_FAIL)
    checks = [
        ('comment-bearing sample is accepted', not accepted),
        ('501-line sample is rejected for the line limit', rejected == ['more than 500 physical lines']),
    ]
    for label, ok in checks:
        print(('ok   ' if ok else 'FAIL ') + label)
    return 0 if all(ok for _, ok in checks) else 1


def main():
    parser = argparse.ArgumentParser(description='Check changed authored files against the contribution rules.')
    parser.add_argument('--base', help='git revision to compare against (BASE...HEAD)')
    parser.add_argument('--selftest', action='store_true', help='run the rule functions on in-memory samples')
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if not args.base:
        parser.error('one of --base or --selftest is required')
    root = Path.cwd().resolve()
    names = subprocess.check_output(['git', 'diff', '--name-only', '--diff-filter=ACMR', '-z', args.base + '...HEAD'], cwd=root).decode().split('\0')
    checked, rejected = 0, 0
    for name in filter(None, names):
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Changed path escapes the checkout')
        relative = path.relative_to(root)
        if relative.parts[0] not in {'src', 'ports', 'public_tools'} and len(relative.parts) != 1:
            continue
        if path.suffix not in {'.py', '.c', '.cpp', '.h', '.hpp', '.s', '.inc'}:
            continue
        checked += 1
        failures = check(path)
        if failures:
            rejected += 1
            print(name + ': ' + ', '.join(failures))
    print('Checked ' + str(checked) + ' changed authored files; rejected ' + str(rejected))
    return int(bool(rejected))


if __name__ == '__main__':
    raise SystemExit(main())
