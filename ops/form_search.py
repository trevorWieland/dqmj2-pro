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
read from the measured branch at the call site (:class:`TargetModes`), and only
then from module-scoped ledger evidence. A Thumb branch's mode is never read from
the compiler's placeholder halfword: mwccarm emits the ``BL`` form for every
interworking call.
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

from thumb_branch import encode as encode_thumb_branch, is_blx  # noqa: E402

FLAGS = ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e',
         '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off',
         '-RTTI', 'off', '-interworking', '-w', 'off', '-sym', 'on', '-gccinc',
         '-nolink', '-msgstyle', 'gcc']
ADDRESS = __import__('re').compile(r'([0-9a-fA-F]{8})$')
SOURCE_ADDRESS = __import__('re').compile(r'native_(?:fn_|data_)?[A-Za-z0-9_]+?_([0-9a-fA-F]{8})$')
# Project naming for measured code symbols (native_fn_<addr>, func_<addr>), used to tell a
# function pointer from a data pointer when setting the ARM ELF Thumb bit on ABS32.
FUNCTION_SYMBOL = __import__('re').compile(r'(?:^|_)(?:fn|func)_')


class TargetModes:
    """Resolve a branch target's instruction set from the measurement image first.

    The compiler emits one ``R_ARM_THM_CALL`` for both a Thumb ``BL`` and an ARM
    ``BLX``; the object's placeholder halfword is always the ``BL`` form. The
    measured image at the *call site* is the only module-local record of which
    form the original linker chose: the second halfword's bit 12 is the
    discriminating marker (BL set, BLX clear). :meth:`resolve_site` reads that
    marker before any ledger evidence.

    Ledger evidence is module-scoped. Base-colliding images are real in this
    project (``arm7-wram`` and ``utility-child-arm7-wram`` both load at
    ``0x037F8000``), so an address alone does not identify a module. A lookup
    therefore considers only the modules whose ranges contain the target, and
    the caller's module wins when it contains the target. There is no global
    address fallback that can borrow another module's row.

    Evidence order for a target without a readable call site:

    1. the ledger row at the target address in a containing module;
    2. a ledger extent containing the target in a containing module;
    3. the ledger row for the target symbol in a containing module;
    4. the containing module's mode when every ledger row in it agrees;
    5. the accepted source file's rule in a containing module;
    6. no evidence: ``None``, and the caller falls back to ``BL``.

    A caller can still pass an explicit ``arm`` hint, which wins over all of the
    above.
    """

    def __init__(self, root, module=None):
        self.root = Path(root)
        self.caller = module
        self.by_module_address = {}
        self.by_module_symbol = {}
        self.module_extents = collections.defaultdict(list)
        self.module_modes = {}
        self.module_ranges = []
        self.module_info = {}
        self.images = {}
        self.source_paths = collections.defaultdict(list)
        self._loaded = False
        self._source_loaded = False
        self._rules = []
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
            if row.get('module'):
                module = row['module']
                self.by_module_address.setdefault((module, address), mode)
                modes_by_module[module].add(mode)
                if row.get('symbol'):
                    self.by_module_symbol.setdefault((module, row['symbol']), mode)
            if row.get('bytes'):
                extent = (address, address + int(row['bytes']), mode)
                if row.get('module'):
                    self.module_extents[row['module']].append(extent)
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
            name = module['name']
            self.module_info[name] = dict(base=base, size=size,
                                          binary=module.get('binary'))
            self.module_ranges.append((size, base, base + size, name))
        # Smallest range first, so an overlay or child image beats a containing
        # program image that shares its base.
        self.module_ranges.sort()

    def _image(self, module):
        """Return ``(bytes, base)`` for one module image, or ``None``."""
        if module in self.images:
            return self.images[module]
        info = self.module_info.get(module)
        result = None
        if info and info.get('binary'):
            path = self.root / info['binary']
            if path.is_file():
                result = (path.read_bytes(), info['base'])
        self.images[module] = result
        return result

    def _modules_containing(self, target):
        """Modules whose image range contains ``target``.

        A target inside the caller's own image is an intra-module target: only
        the caller's ledger rows may describe it, because a base-colliding image
        is indistinguishable by address alone. A target outside the caller image
        is external, and the smallest containing range wins.
        """
        if self.caller and self._caller_contains(target):
            return [self.caller]
        names = []
        for unused_size, start, end, name in self.module_ranges:
            if start <= target < end and name not in names:
                names.append(name)
        return names

    def _caller_contains(self, target):
        for unused_size, start, end, name in self.module_ranges:
            if name == self.caller and start <= target < end:
                return True
        return False

    def _load_source_index(self):
        if self._source_loaded:
            return
        self._source_loaded = True
        config = self.root / 'config/source_units.json'
        if not config.is_file():
            return
        document = json.loads(config.read_text(encoding='utf-8'))
        self._profiles = document.get('flagProfiles', {})
        self._rules = list(document.get('rules', []))
        for path in (self.root / 'src').rglob('*'):
            if path.suffix.lower() not in ('.c', '.s', '.cpp', '.inc') or not path.is_file():
                continue
            match = SOURCE_ADDRESS.search(path.stem)
            if match:
                self.source_paths[int(match.group(1), 16)].append(
                    path.relative_to(self.root).as_posix())

    def _source_evidence(self, relative):
        """Merge every matching rule and return ``(mode, module)``."""
        matched = []
        for index, rule in enumerate(self._rules):
            glob = rule.get('glob', '')
            if glob and fnmatch.fnmatch(relative, glob):
                matched.append((len(glob), index, rule))
        if not matched:
            return None, None
        matched.sort()
        merged = {}
        for unused_length, unused_index, rule in matched:
            for field in ('module', 'mode', 'compilerFlags', 'compilerSha256'):
                if field in rule:
                    merged[field] = rule[field]
        mode = merged.get('mode')
        if mode not in ('arm', 'thumb'):
            flags = merged.get('compilerFlags')
            if isinstance(flags, str):
                flags = self._profiles.get(flags, [])
            mode = 'thumb' if '-thumb' in (flags or []) else 'arm'
        return mode, merged.get('module')

    def _source_mode(self, target, candidates):
        self._load_source_index()
        for relative in self.source_paths.get(target, []):
            mode, module = self._source_evidence(relative)
            if not mode:
                continue
            if not candidates or module is None or module in candidates:
                return mode
        return None

    @staticmethod
    def _containing(extents, target):
        for start, end, mode in extents:
            if start <= target < end:
                return mode
            if start > target:
                break
        return None

    def site_mode(self, site):
        """Read a Thumb BL/BLX marker from the caller's measured image.

        Returns ``'arm'`` for a BLX immediate and ``'thumb'`` for a BL, or
        ``None`` when the site is outside the caller image or does not carry a
        Thumb-2 branch prefix.
        """
        if site is None or not self.caller:
            return None
        self._load()
        pair = self._image(self.caller)
        if pair is None:
            return None
        image, base = pair
        offset = site - base
        if offset < 0 or offset + 4 > len(image):
            return None
        first, second = struct.unpack_from('<HH', image, offset)
        if (first & 0xF800) != 0xF000:
            return None
        return 'arm' if is_blx(second) else 'thumb'

    def image_word(self, site):
        """Read the measured 32-bit word at ``site`` from the caller image."""
        if site is None or not self.caller:
            return None
        self._load()
        pair = self._image(self.caller)
        if pair is None:
            return None
        image, base = pair
        offset = site - base
        if offset < 0 or offset + 4 > len(image):
            return None
        return struct.unpack_from('<I', image, offset)[0]

    def resolve_site(self, site, target=None, symbol=None):
        """Resolve a branch target's mode from the call site, then the ledger."""
        self._load()
        mode = self.site_mode(site)
        if mode:
            return mode, 'image-branch'
        return self.resolve(target, symbol)

    def resolve(self, target, symbol=None):
        """Return ``(mode, evidence)``; mode is ``'arm'``, ``'thumb'`` or ``None``.

        All ledger and source evidence is restricted to modules whose ranges
        contain ``target``. When the caller's module contains the target it is the
        only candidate, so a base-colliding host row cannot win over the child
        image that a child caller is actually linked against.
        """
        self._load()
        candidates = self._modules_containing(target) if target is not None else []
        if not candidates and self.caller:
            candidates = [self.caller]
        if symbol:
            # A symbol name is module-qualified (`func_...` vs
            # `func_utility_child_...`) and is stronger than an address that two
            # base-colliding modules can share.
            for module in candidates:
                mode = self.by_module_symbol.get((module, symbol))
                if mode:
                    return mode, 'ledger-symbol'
        if target is not None:
            for module in candidates:
                mode = self.by_module_address.get((module, target))
                if mode:
                    return mode, 'ledger-address'
            for module in candidates:
                mode = self._containing(self.module_extents.get(module, []), target)
                if mode:
                    return mode, 'ledger-extent'
        if target is not None:
            for module in candidates:
                if module in self.module_modes:
                    return self.module_modes[module], 'module-mode'
            mode = self._source_mode(target, candidates)
            if mode:
                return mode, 'source-file'
        return None, 'fallback'



class UnsupportedRelocation(ValueError):
    """A relocation kind the patcher cannot encode yet.

    Callers that measure many units should pass ``skip_counts`` to
    :func:`relocate` and report the counter. A silently skipped kind is a
    measurement hole, not a source mismatch.
    """

    def __init__(self, kind, offset):
        self.kind = kind
        self.offset = offset
        super().__init__(f'unsupported relocation {kind} at {offset:#x}')


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


def relocate(text, base, relocations, defined, modes=None, arm=None, skip_counts=None):
    """Patch a compiled object's relocations at ``base``.

    ``modes`` is a :class:`TargetModes`; when omitted, Thumb branches fall back to
    ``BL``. ``arm`` is an explicit caller hint (``True``/``False``) that wins over
    the resolved target mode. The object's placeholder halfword is deliberately
    *not* used as evidence: mwccarm always emits the BL form, including for a
    Thumb caller of an ARM callee.

    A Thumb branch is resolved from the measured image at the call site first
    (:meth:`TargetModes.resolve_site`), so a base-colliding module cannot decide
    it. Ledger evidence is module-scoped.

    An ``R_ARM_ABS32`` to a Thumb function carries bit 0, because the ARM ELF symbol
    value does; mwccarm cannot encode the callee's instruction set in a relocatable
    object, so the patcher has to set it the way the linker would. Without it every
    literal pointer to a Thumb function reads back one byte low (nine accepted ov006
    rows compile to exactly that shape, see docs/authoring/permuter.md).

    ``skip_counts``, when given, receives ``kind -> unit count`` for every
    relocation the patcher cannot encode. The exception is still raised; the
    counter is how a scanner reports the hole instead of hiding it.
    """
    out = bytearray(text)
    for offset, kind, symbol, addend in relocations:
        target = defined.get(symbol) or symbol_address(symbol)
        # 16 is R_ARM_THM_XPC22, the BLX-to-ARM form mwcc emits for an
        # interworking call to a symbol outside the translation unit. It is the
        # same two-halfword immediate as 10/30; the measured site decides BLX.
        if kind in (10, 16, 30):
            place = base + offset
            if arm is None:
                if modes is not None:
                    resolver = getattr(modes, 'resolve_site', None)
                    if resolver is not None:
                        mode = resolver(place, target, symbol)[0]
                    else:
                        mode = modes.resolve(target, symbol)[0]
                else:
                    mode = None
            else:
                mode = 'arm' if arm else 'thumb'
            first, second = encode_thumb_branch(place, target, addend, mode=mode)
            struct.pack_into('<H', out, offset, first)
            struct.pack_into('<H', out, offset + 2, second)
        elif kind == 1:  # R_ARM_PC24
            word = struct.unpack_from('<I', out, offset)[0]
            immediate = (target + addend - (base + offset)) >> 2
            struct.pack_into('<I', out, offset,
                             (word & 0xFF000000) | (immediate & 0xFFFFFF))
        elif kind == 2:
            reader = getattr(modes, 'image_word', None) if modes is not None else None
            decoded = reader(base + offset) if reader is not None else None
            if decoded is not None:
                # The measured word is what the original linker wrote. It also
                # disambiguates a symbol address two base-colliding modules share.
                value = decoded
            else:
                value = target + addend
                if (modes is not None and FUNCTION_SYMBOL.search(symbol)
                        and modes.resolve(target, symbol)[0] == 'thumb'):
                    value |= 1
            struct.pack_into('<I', out, offset, value & 0xFFFFFFFF)
        elif kind in (43, 44):  # R_ARM_MOVW_ABS_NC / R_ARM_MOVT_ABS
            value = target + addend
            if kind == 43 and modes is not None and modes.resolve(target, symbol)[0] == 'thumb':
                value |= 1
            immediate = (value & 0xFFFF) if kind == 43 else ((value >> 16) & 0xFFFF)
            word = struct.unpack_from('<I', out, offset)[0]
            word = ((word & ~0x000F0FFF) | ((immediate & 0xF000) << 4)
                    | (immediate & 0x0FFF))
            struct.pack_into('<I', out, offset, word)
        elif kind in (47, 48):  # R_ARM_THM_MOVW_ABS_NC / R_ARM_THM_MOVT_ABS
            value = target + addend
            if kind == 47 and modes is not None and modes.resolve(target, symbol)[0] == 'thumb':
                value |= 1
            immediate = (value & 0xFFFF) if kind == 47 else ((value >> 16) & 0xFFFF)
            first, second = struct.unpack_from('<HH', out, offset)
            first = ((first & ~0x040F) | (((immediate >> 11) & 1) << 10)
                     | ((immediate >> 12) & 0x0F))
            second = ((second & ~0x70FF) | (((immediate >> 8) & 0x07) << 12)
                      | (immediate & 0xFF))
            struct.pack_into('<H', out, offset, first)
            struct.pack_into('<H', out, offset + 2, second)
        else:
            if skip_counts is not None:
                skip_counts[kind] = skip_counts.get(kind, 0) + 1
            raise UnsupportedRelocation(kind, offset)
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
