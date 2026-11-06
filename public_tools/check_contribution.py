import argparse
import io
import re
import subprocess
import tokenize
from pathlib import Path


def check(path):
    text = path.read_text(encoding='utf-8-sig')
    failures = []
    if len(text.splitlines()) > 500:
        failures.append('more than 500 physical lines')
    if path.suffix == '.py':
        comments = any(t.type == tokenize.COMMENT for t in tokenize.generate_tokens(io.StringIO(text).readline))
    else:
        stripped = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '', text)
        comments = bool(re.search(r'//|/\*', stripped))
    if comments:
        failures.append('authored comments belong in documentation')
    return failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', required=True)
    args = parser.parse_args()
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
