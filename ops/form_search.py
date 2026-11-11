"""Enumerate source-form combinations for one row, compile each and keep the best.

Deliberate template design is otherwise "guess the original's memory discipline, one
compile per guess". This tool automates the guessing: give it a C template with
``$NAME`` placeholders, a grid of alternatives per dimension, the row's address, and it
will compile every combination, score each by (differing bytes, length delta) and keep
the best.

    python ops/form_search.py --module ov006 --address 0x021F4C80 --bytes 68 \\
        --template ops/form_specs/021f4c80.c --grid ops/form_specs/021f4c80.json \\
        --symbol native_ov006_021f4c80 [--limit 500] [--keep build/form_search/best.c]

The template uses ``string.Template`` syntax (``$CHANNEL_QUAL``), so ordinary C braces
are left alone. The grid is a JSON object of ``DIMENSION -> [alternative, ...]``; the
search is the full product, capped.

Scoring is prefix-aligned: the number of bytes that differ between the compiled text
and the measured image, then the absolute length difference as a tie-break. A score of
``(0, 0)`` means the combination reproduces the image exactly.

The row's image slice comes from the module image named in ``manifest.json``; branch
relocations are expanded through :mod:`ops.thumb_branch` with the target's mode
resolved by :class:`TargetModes` (ledger address, module, then accepted source
file). A Thumb branch's mode is never read from the compiler's placeholder
halfword: mwccarm emits the ``BL`` form for every interworking call.
"""
import argparse
import collections
import fnmatch
import itertools
import json
import os
import re
import string
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from thumb_branch import encode as encode_thumb_branch  # noqa: E402

FLAGS = ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e',
         '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off',
         '-RTTI', 'off', '-interworking', '-w', 'off', '-sym', 'on', '-gccinc',
         '-nolink', '-msgstyle', 'gcc']
ADDRESS = __import__('re').compile(r'([0-9a-fA-F]{8})$')
SOURCE_ADDRESS = __import__('re').compile(r'native_(?:fn_|data_)?[A-Za-z0-9_]+?_([0-9a-fA-F]{8})$')


class TargetModes:
    """Resolve a Thumb branch target's instruction set from project evidence.

    The compiler emits one ``R_ARM_THM_CALL`` for both a Thumb ``BL`` and an ARM
    ``BLX``; the object's placeholder halfword is always the ``BL`` form. The
    mode therefore has to come from the *target*, strongest evidence first:

    1. the ledger row at the target address (``mode``), or the ledger row whose
       measured extent contains it (a mid-function ARM entry);
    2. the ledger row for the target symbol (name aliases);
    3. the target module's mode when every ledger row in it agrees;
    4. the existing accepted source file's mode (``config/source_units.json``
       rule profile, ``-thumb`` or not);
    5. no evidence: ``None``, and the caller falls back to ``BL``.

    ``relocate`` uses this to encode BLX for ARM targets. A caller can still
    pass an explicit ``arm`` hint, which wins over all of the above.
    """

    def __init__(self, root, module=None):
        self.root = Path(root)
        self.caller = module
        self.by_address = {}
        self.by_module_address = {}
        self.by_symbol = {}
        self.extents = []
        self.module_extents = collections.defaultdict(list)
        self.module_modes = {}
        self.module_ranges = []
        self.source_paths = {}
        self._loaded = False
        self._source_loaded = False
        self._exact_rules = {}
        self._wildcard_rules = []
        self._profiles = {}

    def _load(self):
        if self._loaded:
            return
        self._loaded = True
        ledger = self.root / 'ledger/functions.jsonl'
        modes_by_module = collections.defaultdict(set)
        rows = []
        if ledger.is_file():
            with ledger.open(encoding='utf-8') as stream:
                for line in stream:
                    line = line.strip()
                    if line:
                        rows.append(json.loads(line))
        for row in rows:
            mode = row.get('mode')
            if mode not in ('arm', 'thumb'):
                continue
            address = int(row['address'], 0)
            self.by_address.setdefault(address, mode)
            if row.get('module'):
                self.by_module_address.setdefault((row['module'], address), mode)
                modes_by_module[row['module']].add(mode)
            if row.get('bytes'):
                self.extents.append((address, address + int(row['bytes']), mode))
                if row.get('module'):
                    self.module_extents[row['module']].append(
                        (address, address + int(row['bytes']), mode))
            if row.get('symbol'):
                self.by_symbol.setdefault(row['symbol'], mode)
        self.extents.sort()
        for extents in self.module_extents.values():
            extents.sort()
        for module, modes in modes_by_module.items():
            if len(modes) == 1:
                self.module_modes[module] = next(iter(modes))
        self._load_module_ranges()

    def _load_module_ranges(self):
        manifest = self.root / 'manifest.json'
        if not manifest.is_file():
            return
        document = json.loads(manifest.read_text(encoding='utf-8-sig'))
        for module in document.get('modules', []):
            size = module.get('bytes')
            if type(size) is not int or size <= 0 or 'base' not in module:
                continue
            base = int(str(module['base']), 0)
            self.module_ranges.append((size, base, base + size, module['name']))
        # Smallest range first, so an overlay beats a containing program image.
        self.module_ranges.sort()

    def _load_source_index(self):
        if self._source_loaded:
            return
        self._source_loaded = True
        config = self.root / 'config/source_units.json'
        if not config.is_file():
            return
        document = json.loads(config.read_text(encoding='utf-8'))
        self._profiles = document.get('flagProfiles', {})
        self._wildcard_rules = [rule for rule in document.get('rules', [])
                                if any(char in rule.get('glob', '') for char in '*?[')]
        self._wildcard_rules.sort(key=lambda rule: len(rule['glob']), reverse=True)
        for rule in document.get('rules', []):
            glob = rule.get('glob', '')
            if glob and not any(char in glob for char in '*?['):
                self._exact_rules[glob] = rule
        for path in (self.root / 'src').rglob('*'):
            if path.suffix.lower() not in ('.c', '.s', '.cpp', '.inc') or not path.is_file():
                continue
            match = SOURCE_ADDRESS.search(path.stem)
            if match:
                self.source_paths.setdefault(int(match.group(1), 16),
                                             path.relative_to(self.root).as_posix())

    def _rule_mode(self, relative):
        rule = self._exact_rules.get(relative)
        if rule is None:
            for candidate in self._wildcard_rules:
                if fnmatch.fnmatch(relative, candidate['glob']):
                    rule = candidate
                    break
        if rule is None:
            return None
        if rule.get('mode') in ('arm', 'thumb'):
            return rule['mode']
        flags = self._profiles.get(rule.get('compilerFlags'), [])
        return 'thumb' if '-thumb' in flags else 'arm'

    def _module_of(self, target):
        for unused_size, start, end, name in self.module_ranges:
            if start <= target < end:
                return name
        return None

    @staticmethod
    def _containing(extents, target):
        for start, end, mode in extents:
            if start <= target < end:
                return mode
            if start > target:
                break
        return None

    def resolve(self, target, symbol=None):
        """Return ``(mode, evidence)``; mode is ``'arm'``, ``'thumb'`` or ``None``."""
        self._load()
        if target is not None and self.caller:
            mode = self.by_module_address.get((self.caller, target))
            if mode:
                return mode, 'ledger-address'
            mode = self._containing(self.module_extents.get(self.caller, []), target)
            if mode:
                return mode, 'ledger-extent'
        if target is not None:
            mode = self.by_address.get(target)
            if mode:
                return mode, 'ledger-address'
            mode = self._containing(self.extents, target)
            if mode:
                return mode, 'ledger-extent'
        if symbol:
            mode = self.by_symbol.get(symbol)
            if mode:
                return mode, 'ledger-symbol'
        if target is not None:
            module = self._module_of(target)
            if module and module in self.module_modes:
                return self.module_modes[module], 'module-mode'
            self._load_source_index()
            relative = self.source_paths.get(target)
            if relative:
                mode = self._rule_mode(relative)
                if mode:
                    return mode, 'source-file'
        return None, 'fallback'



def default_compiler(root):
    return Path(os.environ.get('DSH_MWCC',
                              str(root / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')))


def module_image(root, name):
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8-sig'))
    for module in manifest['modules']:
        if module['name'] == name:
            path = root / module['binary']
            base = int(str(module['base']), 0)
            return path.read_bytes(), base, base
    raise SystemExit(f'unknown module: {name}')


def symbol_address(name):
    match = ADDRESS.search(name)
    if not match:
        raise ValueError(f'external symbol has no measured address: {name}')
    return int(match.group(1), 16)


def compile_source(cc, source, obj, root, flags=None):
    env = dict(os.environ, LM_LICENSE_FILE=str(root / 'tools/mwccarm/mwccarm/license.dat'))
    # -thumb has to precede -c: mwcc reads the mode flag before the compile action.
    return subprocess.run([str(cc), *(flags or FLAGS), '-thumb', '-c', str(source),
                           '-o', str(obj)], capture_output=True, text=True, env=env)


def read_object(obj):
    from elftools.elf.elffile import ELFFile
    with open(obj, 'rb') as stream:
        elf = ELFFile(stream)
        text = elf.get_section_by_name('.text').data()
        symtab = elf.get_section_by_name('.symtab')
        defined = {}
        for symbol in symtab.iter_symbols():
            section = symbol['st_shndx']
            if isinstance(section, int) and section != 'SHN_UNDEF' and symbol['st_value']:
                defined[symbol.name] = symbol['st_value']
        relocations = []
        # Only the relocations that apply to the function body. mwcc emits RELA
        # (``.rela.text``) for these objects, but accept the REL spelling too; the
        # ``.rel.debug_*`` sections carry section symbols that would never resolve.
        wanted = {'.rel.text', '.rela.text'}
        for section in elf.iter_sections():
            if section.name not in wanted:
                continue
            for relocation in section.iter_relocations():
                symbol = symtab.get_symbol(relocation['r_info_sym']).name
                addend = relocation['r_addend'] if section.name == '.rela.text' else 0
                relocations.append((relocation['r_offset'], relocation['r_info_type'],
                                    symbol, addend or 0))
    return text, defined, relocations


def relocate(text, base, relocations, defined, modes=None, arm=None):
    """Patch a compiled object's relocations at ``base``.

    ``modes`` is a :class:`TargetModes`; when omitted, Thumb branches fall back to
    ``BL``. ``arm`` is an explicit caller hint (``True``/``False``) that wins over
    the resolved target mode. The object's placeholder halfword is deliberately
    *not* used as evidence: mwccarm always emits the BL form, including for a
    Thumb caller of an ARM callee.
    """
    out = bytearray(text)
    for offset, kind, symbol, addend in relocations:
        target = defined.get(symbol) or symbol_address(symbol)
        if kind in (10, 30):
            place = base + offset
            if arm is None:
                mode = modes.resolve(target, symbol)[0] if modes is not None else None
            else:
                mode = 'arm' if arm else 'thumb'
            first, second = encode_thumb_branch(place, target, addend, mode=mode)
            struct.pack_into('<H', out, offset, first)
            struct.pack_into('<H', out, offset + 2, second)
        elif kind == 2:
            struct.pack_into('<I', out, offset, (target + addend) & 0xFFFFFFFF)
        else:
            raise ValueError(f'unsupported relocation {kind} at {offset:#x}')
    return bytes(out)


def score(actual, want):
    differing = sum(1 for a, b in zip(actual, want) if a != b)
    differing += abs(len(actual) - len(want))
    return differing, abs(len(actual) - len(want))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--address', required=True)
    parser.add_argument('--bytes', type=int, required=True)
    parser.add_argument('--symbol', required=True)
    parser.add_argument('--template', required=True)
    parser.add_argument('--grid', required=True)
    parser.add_argument('--limit', type=int, default=500)
    parser.add_argument('--top', type=int, default=5, help='keep this many ranked combinations')
    parser.add_argument('--keep', help='write the winning source here')
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--work', default=None)
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    address = int(args.address, 0)
    image, _, base = module_image(root, args.module)
    want = image[address - base: address - base + args.bytes]
    template = string.Template(Path(args.template).read_text(encoding='utf-8'))
    grid = json.loads(Path(args.grid).read_text(encoding='utf-8'))
    cc = default_compiler(root)
    modes = TargetModes(root, args.module)
    work = Path(args.work or root / 'build/form_search')
    work.mkdir(parents=True, exist_ok=True)

    names = list(grid)
    combinations = list(itertools.product(*(grid[name] for name in names)))
    print(f'dimensions: {len(names)} ({", ".join(names)})')
    print(f'combinations: {len(combinations)}; limit {args.limit}')
    best = None
    ranked = []
    tried = 0
    for combination in combinations[:args.limit]:
        values = dict(zip(names, combination))
        source = template.substitute(values)
        path = work / 'candidate.c'
        path.write_text(source, encoding='utf-8')
        compiled = compile_source(cc, path, work / 'candidate.o', root)
        tried += 1
        if compiled.returncode != 0:
            if tried == 1:
                print('first compile failed:', (compiled.stderr or compiled.stdout).strip()[:300])
            continue
        text, defined, relocations = read_object(work / 'candidate.o')
        try:
            actual = relocate(text, address, relocations, defined, modes=modes)
        except ValueError:
            continue
        current = score(actual, want)
        ranked.append((current, dict(values), len(actual)))
        ranked.sort(key=lambda item: item[0])
        del ranked[args.top:]
        if best is None or current < best[0]:
            best = (current, values, actual)
            print(f'  #{tried:3d} best {current}: ' + ', '.join(f'{k}={v!r}' for k, v in values.items())[:150])
    if best is None:
        print('no combination compiled')
        return 2
    (differing, length), values, actual = best
    print(f'\ntried {tried} combinations; best score {best[0]} '
          f'({"EXACT" if best[0] == (0, 0) else "not exact"})')
    for key, value in values.items():
        print(f'  {key} = {value!r}')
    print(f'  length: compiled {len(actual)} B, image {len(want)} B')
    print('\nranked table (score, length):')
    for rank, (current, values, length) in enumerate(ranked, 1):
        rendered = ', '.join(f'{key}={value!r}' for key, value in values.items()
                             if '\n' not in str(value))
        print(f'  {rank}. {current} len={length}  {rendered[:160]}')
    if args.keep:
        Path(args.keep).write_text(template.substitute(values), encoding='utf-8')
        print(f'winning source: {args.keep}')
    return 0 if best[0] == (0, 0) else 1


if __name__ == '__main__':
    sys.exit(main())
