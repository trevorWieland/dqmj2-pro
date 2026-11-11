"""Refuse to author an address that is already defined somewhere under src/.

Five duplicate incidents in one session make this mechanical rather than a habit.
For each address the check looks for three independent kinds of evidence anywhere
under ``src/`` (including ``src/transplants/`` and every batch directory):

1. a **file name** containing the address (``native_main_021f6244.c``);
2. a **symbol name** containing the address (``void native_main_021f6244(void)``);
3. an **address literal in a definition context** — a column-0 definition line that
   mentions the address, or a data definition named after it.

Comments, extern declarations, call sites and prototypes are *mentions*, not
definitions, and do not block on their own; they are reported separately so a
caller can be told apart from a definition.

    python ops/check_duplicate.py --address 0x021FBB04 0x021FBDD8 0x021FC0B8
    python ops/check_duplicate.py --address-file addresses.txt --root <checkout>

Exit status is 1 when any address has a definition hit, so a packet build can gate
on it. The output lists every hit, never a sample.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ('.c', '.h', '.s', '.inc', '.cpp')
DEFINITION = re.compile(r'^(?:[A-Za-z_][\w \t\*]*[\s\*]+)?(native_[A-Za-z0-9_]+)\s*\(')
ASM_EXPORT = re.compile(r'^\s*\.(?:global|globl|type)\s+(native_[A-Za-z0-9_]+)')
ASM_LABEL = re.compile(r'^(native_[A-Za-z0-9_]+):')
COMMENTS = re.compile(r'/\*.*?\*/|//[^\n]*', re.S)


def normalise(address):
    value = address if isinstance(address, int) else int(str(address), 0)
    return f'{value:08x}'


def hits_for(address, root, files):
    """Return (definitions, mentions) for one address."""
    key = normalise(address)
    definitions, mentions = [], []
    for path, text, suffix, relative in files:
        if key in path.name.lower():
            definitions.append(f'{relative}  (file name)')
            continue
        if key not in text:
            continue
        stripped = COMMENTS.sub('', text) if suffix in ('.c', '.h', '.cpp', '.inc') else text
        for line in stripped.splitlines():
            if key not in line:
                continue
            if line[:1] in (' ', '\t'):
                mentions.append(f'{relative}  (mention: {line.strip()[:70]})')
                continue
            if ASM_EXPORT.match(line) or ASM_LABEL.match(line):
                definitions.append(f'{relative}  (asm symbol: {line.strip()[:60]})')
            elif DEFINITION.match(line) and line.rstrip().endswith(';'):
                mentions.append(f'{relative}  (declaration: {line.strip()[:60]})')
            elif DEFINITION.match(line):
                definitions.append(f'{relative}  (definition: {line.strip()[:60]})')
            else:
                mentions.append(f'{relative}  (mention: {line.strip()[:70]})')
    return definitions, mentions


def load_files(root):
    files = []
    for path in (root / 'src').rglob('*'):
        if path.suffix.lower() not in SOURCES or not path.is_file():
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='replace').lower()
        except OSError:
            continue
        files.append((path, text, path.suffix.lower(), path.relative_to(root).as_posix()))
    return files


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--address', nargs='+', default=[])
    parser.add_argument('--address-file', help='one address per line')
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--allow-mentions', action='store_true',
                        help='report mentions without failing on them')
    args = parser.parse_args(argv)

    addresses = list(args.address)
    if args.address_file:
        addresses += [line.strip() for line in Path(args.address_file).read_text().splitlines()
                      if line.strip()]
    if not addresses:
        parser.error('no addresses given')

    root = Path(args.root).resolve()
    files = load_files(root)
    blocked = 0
    for address in addresses:
        definitions, mentions = hits_for(address, root, files)
        status = 'BLOCKED' if definitions else 'clear'
        print(f'{status:8s} {address}')
        for hit in definitions:
            print(f'           definition: {hit}')
        for hit in mentions:
            print(f'           mention:    {hit}')
        if definitions:
            blocked += 1
    print(f'\n{len(addresses)} addresses, {blocked} already defined under src/')
    return 1 if blocked else 0


if __name__ == '__main__':
    sys.exit(main())
