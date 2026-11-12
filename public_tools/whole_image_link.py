"""Whole-image ARM9 link and byte-diff gate.

This is the verification gate the project goal names as required: link *every* accepted
main-module source file into the ARM9 module's declared section layout with the pinned
Metrowerks toolchain, then prove by byte diff which parts of the reconstructed image are
real.

Three things distinguish this from the unit-level measurement in ``repo_build.py``:

1.  **One link, one image.**  Every reconstructed object is placed at the absolute address
    the address ledger measured for it, inside a linker command file whose region origins
    and section boundaries come from the module's own section table
    (``config/arm9/delinks.txt``) cross-checked against the private module header
    (``extract/arm9/arm9.yaml``).  The linker writes the ARM9 region straight to a flat
    binary of the module's declared size.
2.  **Nothing is patched.**  ``repo_build`` resolves a function's relocations from the
    original image so it can measure one function in isolation.  This tool does the
    opposite: it hands the linker a symbol table taken from ``config/arm9/symbols.txt``
    and the ledger, so the bytes in the image are the bytes the linker produced.
3.  **The diff is the verdict.**  A reconstructed function passes only when its linked
    bytes equal the extracted image byte for byte.  Everything that differs must fall in a
    span with no reconstructed source (a stub) or in a real hole; a difference anywhere
    else is a gate failure.

Command lines::

    python public_tools/whole_image_link.py --root . --out build/whole-image
    python public_tools/whole_image_link.py --root . --emit-lcf
    python public_tools/whole_image_link.py --root . --check-lcf

The linker command file is written to ``ports/recompile/arm9.lcf``.  ``--emit-lcf``
regenerates it and ``--check-lcf`` fails when the committed file no longer matches the
tree.
"""

import argparse
import bisect
import collections
import concurrent.futures
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from repo_build import elf_profile, pair_functions, short_paths  # noqa: E402
from source_units import CONFIG, config_digest, enumerate_sources, load_config  # noqa: E402

MODULE = 'main'
PROCESSOR = 'arm9'
LCF_PATH = 'ports/recompile/arm9.lcf'
BASELINE_PATH = 'ports/recompile/arm9-baseline.json'
LEDGER_PATH = 'ledger/functions.jsonl'
IMAGE_PATH = 'extract/arm9/arm9.bin'
HEADER_PATH = 'extract/arm9/arm9.yaml'
ROM_PATH = 'inputs/game.nds'
ROM_SHA256 = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
ROM_BYTES = 175959612
DELINKS_PATH = 'config/arm9/delinks.txt'
SYMBOLS_PATH = 'config/arm9/symbols.txt'
TOOLCHAIN = 'tools/mwccarm/mwccarm/2.0/base'
ASSEMBLER_PROCESSOR = 'arm5TE'
IDENTIFIER = re.compile(r'^[A-Za-z_$][A-Za-z0-9_$]*$')
ADDRESS_SUFFIX = re.compile(r'(?:^|_)([0-9a-fA-F]{7,8})$')
DELINK = re.compile(r'^\s+\.(\S+)\s+start:(0x[0-9a-fA-F]+)\s+end:(0x[0-9a-fA-F]+)'
                    r'\s+kind:(code|data|rodata|bss)\s+align:(\d+)\s*$')
SYMBOL = re.compile(r'^(\S+)\s+kind:(\w+)(?:\(([^)]*)\))?\s+addr:(0x[0-9a-fA-F]+)\s*$')
SYMBOL_SIZE = re.compile(r'size=(0x[0-9a-fA-F]+)')
EXECUTABLE = 0x4
ALLOCATABLE = 0x2


class WholeImageError(ValueError):
    pass


def digest(path):
    hasher = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            hasher.update(block)
    return hasher.hexdigest()


_ELF_CACHE = {}


def read_elf(path):
    """Read and parse one object once; a full run touches every object several times.

    Only the aggregates the plan needs are kept: the function headings without their bytes,
    the section table without its payloads, and the three name sets.  Caching whole profiles
    for five thousand objects costs gigabytes, which is how this gate first died.
    """
    key = str(path)
    stat = os.stat(key)
    stamp = (stat.st_size, stat.st_mtime_ns)
    cached = _ELF_CACHE.get(key)
    if cached is not None and cached[0] == stamp:
        return cached[1]
    raw = Path(key).read_bytes()
    profile = elf_profile(raw)
    value = dict(
        functions=[dict(name=item['name'], value=item['value'], size=item['size'],
                        section=item['section'], mode=item['mode'])
                   for item in profile['functions']],
        sections=[dict(name=item['name'], type=item['type'], flags=item['flags'],
                       size=item['size']) for item in profile['sections']],
        globals=global_definitions(raw), undefined=undefined_names(raw),
        defined=linked_symbols(raw))
    _ELF_CACHE[key] = (stamp, value)
    return value


def hexint(value):
    return int(value, 0) if isinstance(value, str) else int(value)


def note(message):
    """Progress on stderr, flushed: a full link takes long enough to need a trace."""
    print('whole-image: ' + message, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# Module layout: the section table, its header cross-check, and the LCF renderer


def load_layout(root):
    """Read the module's measured section table.

    ``config/arm9/delinks.txt`` is the delinked extent of the main module exactly as the
    original link produced it: each line is ``.<name> start:0x.. end:0x.. kind:.. align:..``.
    It is committed, so the layout half of the linker command file is reproducible from
    public data alone.
    """
    path = Path(root) / DELINKS_PATH
    if not path.is_file():
        raise WholeImageError('The module section table is unavailable: ' + DELINKS_PATH)
    sections = []
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        match = DELINK.match(line)
        if not match:
            raise WholeImageError('Unparsed section-table line: ' + line.strip())
        sections.append(dict(name=match[1], start=hexint(match[2]), end=hexint(match[3]),
                             kind=match[4], align=int(match[5])))
    if not sections:
        raise WholeImageError('The module section table is empty')
    by_name = {section['name']: section for section in sections}
    for required in ('text', 'rodata', 'ctor', 'data', 'bss'):
        if required not in by_name:
            raise WholeImageError('The module section table has no .' + required)
    previous = None
    for section in sections:
        if section['end'] < section['start']:
            raise WholeImageError('Section .%s ends before it starts' % section['name'])
        if previous is not None and section['start'] < previous['end']:
            raise WholeImageError('Section .%s overlaps the previous section' % section['name'])
        previous = section
    return dict(sections=sections, byName=by_name)


def check_header(root, layout):
    """Cross-check the section table against the private module header.

    ``extract/arm9/arm9.yaml`` is written by the extractor from the module header: it
    carries the load address, the size of the initialised image and the bss window.  The
    linker command file must agree with both sources or the gate measures the wrong bytes.
    """
    text, data, bss = layout['byName']['text'], layout['byName']['data'], layout['byName']['bss']
    # The initialised image stops at .data end, which the section table places exactly at
    # .bss start; .bss is reserved RAM and is not part of the file.
    expected = dict(base=text['start'], bytes=data['end'] - text['start'],
                    bssStart=bss['start'], bssEnd=bss['end'])
    path = Path(root) / HEADER_PATH
    notes = []
    if path.is_file():
        observed = {}
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            if ':' not in line:
                continue
            key, _, value = line.partition(':')
            try:
                observed[key.strip()] = int(value.strip(), 0)
            except ValueError:
                continue
        for header_key, expected_key in (('base_address', 'base'), ('bss_start', 'bssStart'),
                                         ('bss_end', 'bssEnd')):
            value = observed.get(header_key)
            if value is None:
                notes.append(dict(check='header.' + header_key, status='absent'))
            elif value != expected[expected_key]:
                raise WholeImageError('Module header %s 0x%08x disagrees with the section table 0x%08x'
                                      % (header_key, value, expected[expected_key]))
            else:
                notes.append(dict(check='header.' + header_key, status='agrees',
                                  value='0x%08x' % value))
    else:
        notes.append(dict(check='header', status='absent', path=HEADER_PATH))
    image = Path(root) / IMAGE_PATH
    if image.is_file():
        size = image.stat().st_size
        if size != expected['bytes']:
            raise WholeImageError('Extracted image is %d bytes, the section table declares %d'
                                  % (size, expected['bytes']))
        notes.append(dict(check='image.size', status='agrees', bytes=size))
    else:
        notes.append(dict(check='image', status='absent', path=IMAGE_PATH))
    return expected, notes


def render_lcf(layout, spans, region_file, provenance):
    """Render the linker command file.

    Every directive carries the place its number came from.  ``spans`` is the ordered list
    of ``{address, object, symbol, size, mode, source}`` placements; ``address`` is the
    absolute run address the ledger measured, which the Metrowerks linker accepts as an
    absolute location-counter assignment (``. = 0x02000088;``).
    """
    text, rodata, ctor = layout['byName']['text'], layout['byName']['rodata'], layout['byName']['ctor']
    data, bss = layout['byName']['data'], layout['byName']['bss']
    base = text['start']
    lines = []
    add = lines.append
    rule = '# ' + '=' * 98
    add(rule)
    add('# ports/recompile/arm9.lcf -- whole-image ARM9 linker command file')
    add(rule)
    add('#')
    add('# GENERATED FILE.  Regenerate with:')
    add('#     python public_tools/whole_image_link.py --root . --emit-lcf')
    add('# and verify it is current with:')
    add('#     python public_tools/whole_image_link.py --root . --check-lcf')
    add('#')
    add('# Every address, length and alignment below is derived; nothing is typed by hand.')
    add('#')
    add('#   section table     %s' % DELINKS_PATH)
    add('#                     sha256 %s' % provenance.get('delinksSha256', ''))
    add('#   module header     %s  (base_address, bss_start, bss_end)' % HEADER_PATH)
    add('#   function spans    %s  (address + size per function)' % LEDGER_PATH)
    add('#   symbol addresses  %s  (absolute symbol carrier)' % SYMBOLS_PATH)
    add('#   dialect           the `dsd lcf` output dsd 0.12.1 generates for this project,')
    add('#                     which is the Metrowerks LCF dialect the pinned mwldarm accepts:')
    add('#                     `MEMORY { R : ORIGIN = 0x.. > file }`, `AFTER(..)`,')
    add('#                     `SECTIONS { .name : { ... } > R }`, `ALIGNALL(n)`,')
    add('#                     `. = ALIGN(n)`, `. = 0xADDR`, `WRITEW(v)`, `SYM = .`,')
    add('#                     `ADDR(R)`, `SIZEOF(R)`, `KEEP_SECTION`, `* (.section)` and')
    add('#                     `object.o (.section)` placement.')
    add('#')
    add('# The ARM9 region is written straight to a flat binary by mwldarm, so the link')
    add('# product is the module image itself, not an ELF a second tool must convert.')
    add('#')
    add('# Run it from the directory the objects live in, because a Metrowerks command file')
    add('# can only name an input object by bare file name (a path separator makes the')
    add('# parser report "File not found: build"):')
    add('#     cd build/whole-image')
    add('#     mwldarm -nostdlib -nodeadstrip @objects.rsp')
    add('# `public_tools/whole_image_link.py` does exactly that; this file is its output.')
    add('#')
    add('# Measured layout (from the section table, .text/.rodata/.ctor/.data/.bss order):')
    for section in layout['sections']:
        add('#   .%-8s 0x%08x .. 0x%08x  %7d bytes  kind=%-6s align=%d'
            % (section['name'], section['start'], section['end'],
               section['end'] - section['start'], section['kind'], section['align']))
    add('#')
    add('# The initialised image is .text through .data: 0x%08x .. 0x%08x = %d bytes,'
        % (base, data['end'], data['end'] - base))
    add('# which is the size of extract/arm9/arm9.bin and the length the region file gets.')
    add('#')
    add('# Absolute placements: %d reconstructed spans.' % len(spans))
    add('# Each span is `. = <measured address>; <object>(.text)`.  A function with no')
    add('# reconstructed source is not placed at all: the linker leaves zero bytes in the')
    add('# hole, the next span keeps its absolute address, and the diff reports the hole.')
    add('# Nothing is copied from the image, so a hole cannot fake a match.')
    add('#')
    add(rule)
    add('')
    add('MEMORY {')
    add('    # The whole initialised main module, written as a flat binary.  ORIGIN is the')
    add('    # .text start from the section table; the length is fixed by the final')
    add('    # `. = 0x%08x` in .arm9, which is the .data end / .bss start.' % bss['start'])
    add('    ARM9 : ORIGIN = 0x%08x > %s' % (base, region_file))
    add('    # .bss is not part of the initialised image, so its region names no output file:')
    add('    # mwldarm reserves the address window and writes nothing for it.')
    add('    BSS  : ORIGIN = 0x%08x' % bss['start'])
    add('}')
    add('')
    add('KEEP_SECTION {')
    add('    .init,')
    add('    .ctor,')
    add('    .exceptix')
    add('}')
    add('')
    add('SECTIONS {')
    add('    # Linker-defined bounds, so a startup or a checker can read them without hard-')
    add('    # coding anything: every value is an address from the section table.')
    add('    __ARM9_LO        = 0x%08x;   # .text start' % text['start'])
    add('    __ARM9_TEXT_HI   = 0x%08x;   # .text end' % text['end'])
    add('    __ARM9_RODATA_LO = 0x%08x;   # .rodata start' % rodata['start'])
    add('    __ARM9_DATA_LO   = 0x%08x;   # .data start' % data['start'])
    add('    __ARM9_BSS_LO    = 0x%08x;   # .bss start' % bss['start'])
    add('    __ARM9_HI        = 0x%08x;   # .bss end' % bss['end'])
    add('')
    add('    .arm9 : {')
    add('        ALIGNALL(2);                  # The floor is 2, not 4: 13 of the module\'s')
    add('                                      # functions start at a 2-mod-4 address, so a')
    add('                                      # 4-byte floor would push every Thumb function')
    add('                                      # two bytes past its measured address.  Each')
    add('                                      # placed object has its declared .text align-')
    add('                                      # ment relaxed to the natural alignment of its')
    add('                                      # measured address, so the linker never re-')
    add('                                      # aligns a span away from its placement.')
    add('        . = 0x%08x;                  # .text start (section table)' % text['start'])
    add('        ARM9_TEXT_START = .;')
    for span in spans:
        add('        . = 0x%08x; %s (.text)  # %s %s %d B'
            % (span['address'], span['object'], span['symbol'], span['mode'], span['size']))
    add('        . = 0x%08x;                  # .text end (section table)' % text['end'])
    add('        ARM9_TEXT_END = .;')
    add('')
    add('        ALIGNALL(4);')
    add('        . = 0x%08x;                  # .rodata start (section table)' % rodata['start'])
    add('        ARM9_RODATA_START = .;')
    add('        * (.rodata)                   # reconstructed objects\' own rodata only.  The')
    add('                                      # module\'s real .rodata is not reconstructed, so')
    add('                                      # the rest of this window stays zero.')
    add('        . = 0x%08x;                  # .rodata end (section table)' % rodata['end'])
    add('        ARM9_RODATA_END = .;')
    add('')
    add('        . = 0x%08x;                  # .ctor start (section table)' % ctor['start'])
    add('        ARM9_CTOR_START = .;')
    add('        . = 0x%08x;                  # .ctor end: the section table records .ctor' % ctor['end'])
    add('                                      # as empty, so no terminator word is written.')
    add('        ARM9_CTOR_END = .;')
    add('')
    add('        ALIGNALL(4);')
    add('        . = 0x%08x;                  # .data start (section table).  .data is' % data['start'])
    add('                                      # 32-aligned, which is why this is 0x10 past')
    add('                                      # the .ctor end.')
    add('        ARM9_DATA_START = .;')
    add('        * (.data)                     # reconstructed objects\' own data only.')
    add('        . = 0x%08x;                  # .data end == .bss start; this fixes the' % data['end'])
    add('                                      # written length at 0x%08x bytes.' % (data['end'] - base))
    add('        ARM9_DATA_END = .;')
    add('    } > ARM9')
    add('')
    add('    .bss : {')
    add('        ALIGNALL(2);')
    add('        . = 0x%08x;                  # .bss start (section table)' % bss['start'])
    add('        ARM9_BSS_START = .;')
    add('        * (.bss)')
    add('        * (COMMON)')
    add('        . = 0x%08x;                  # .bss end (section table)' % bss['end'])
    add('        ARM9_BSS_END = .;')
    add('    } > BSS')
    add('}')
    add('')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Source units and objects


def main_units(root, config):
    """Every accepted main-module source file, split into C and assembly."""
    enumerated = enumerate_sources(root, config)
    compiled = [unit for unit in enumerated['compiled']
                if unit['module'] == MODULE and unit['path'].endswith('.c')]
    assembly = [unit for unit in enumerated['assembly'] if unit['module'] == MODULE]
    compiled.sort(key=lambda unit: unit['path'])
    assembly.sort(key=lambda unit: unit['path'])
    return compiled, assembly


def object_relative(key):
    """A stable, short object path for one (source, profile) pair.

    The key is the source path plus the compile profile the ledger records, because the same
    source is sometimes accepted under more than one set of flags.  Nothing here depends on
    ordering, so the linker command file is reproducible.
    """
    # The Metrowerks linker command file can only name an input object by a bare file name
    # (a path separator makes the LCF parser report "File not found: <first component>"),
    # so every object lives flat beside the linker command file.
    return 'build/whole-image/%s.o' % hashlib.sha1(key.encode()).hexdigest()[:10]


def profile_key(path, compiler, flags):
    return path + '|' + str(compiler) + '|' + ','.join(flags)


def unit_profiles(units, ledger):
    """Pick the compile profile for each unit from what the ledger recorded.

    When every matched row of a source names the same profile, that profile is the one that
    produced the accepted object.  When they disagree, the source-unit rule's profile is used
    and only the rows that agree with it can be placed; the rest stay stubs.
    """
    recorded = collections.defaultdict(set)
    for row in ledger:
        if not row['source'] or not row['compilerFlags']:
            continue
        recorded[row['source']].add((row['compilerSha256'], tuple(row['compilerFlags'])))
    chosen = {}
    for unit in units:
        candidates = recorded.get(unit['path'], set())
        rule = (unit['compilerSha256'], tuple(unit.get('compilerFlags') or ()))
        if len(candidates) == 1:
            profile = next(iter(candidates))
            chosen[unit['path']] = dict(compilerSha256=profile[0] or rule[0],
                                        compilerFlags=list(profile[1]),
                                        sourceOfTruth='ledger')
        else:
            chosen[unit['path']] = dict(compilerSha256=rule[0], compilerFlags=list(rule[1]),
                                        sourceOfTruth='source-unit-rule')
        chosen[unit['path']]['distinctLedgerProfiles'] = len(candidates)
    return chosen


def natural_alignment(address):
    """The largest power of two that divides an address; 4 for ARM, 2 for a Thumb start."""
    if address % 4 == 0:
        return 4
    if address % 2 == 0:
        return 2
    return 1


def relax_object_alignment(path, alignment):
    """Lower the declared alignment of an object's executable sections.

    The Metrowerks linker honours an input section's ``sh_addralign`` even when the location
    counter points at a lower-aligned address: a Thumb function measured at ``0x020000f6``
    would be emitted at ``0x020000f8`` and its displacement would corrupt the diff for the
    whole window behind it.  The measured address is authoritative -- the bytes are copied
    verbatim either way -- so the declared alignment is relaxed to what the address needs.
    """
    raw = bytearray(Path(path).read_bytes())
    if raw[:7] != b'\x7fELF\x01\x01\x01':
        raise WholeImageError('Not an ARM ELF32 object: ' + str(path))
    header = struct.unpack_from('<16sHHIIIIIHHHHHH', raw)
    shoff, shentsize, shnum, shstrndx = header[6], header[11], header[12], header[13]
    sections = [struct.unpack_from('<IIIIIIIIII', raw, shoff + shentsize * index)
                for index in range(shnum)]
    names = raw[sections[shstrndx][4]:sections[shstrndx][4] + sections[shstrndx][5]]
    changed = []
    for index, section in enumerate(sections):
        if section[1] not in (1,) or not section[2] & EXECUTABLE:
            continue
        end = names.find(b'\0', section[0])
        name = names[section[0]:end].decode('utf-8', 'replace')
        if section[8] > alignment:
            struct.pack_into('<I', raw, shoff + shentsize * index + 32, alignment)
            changed.append(dict(section=name, was=section[8], now=alignment))
    if changed:
        Path(path).write_bytes(bytes(raw))
    return changed


def toolchain_paths(root, config):
    compilers = {}
    for identity, relative in config['compilers'].items():
        path = Path(root) / relative
        if not path.is_file():
            raise WholeImageError('Pinned compiler is unavailable: ' + relative)
        compilers[identity] = path
    base = Path(root) / TOOLCHAIN
    linker, assembler = base / 'mwldarm.exe', base / 'mwasmarm.exe'
    for tool in (linker, assembler):
        if not tool.is_file():
            raise WholeImageError('Pinned tool is unavailable: ' + str(tool))
    license_file = None
    for candidate in (base.parent.parent.parent / 'license.dat',
                      base.parent.parent / 'license.dat', base / 'license.dat'):
        if candidate.is_file():
            license_file = candidate
            break
    return compilers, assembler, linker, license_file


def compile_units(root, units, compilers, assembler, out, jobs, timeout=240):
    """Compile or assemble each unit into its stable object path."""
    root = Path(root)
    out = root / out
    env = dict(os.environ)
    env.setdefault('MWLibraries', str(root / TOOLCHAIN))
    env.pop('MWLibraryFiles', None)
    (out).mkdir(parents=True, exist_ok=True)

    def build(unit):
        source = (root / unit['path']).resolve()
        profile = unit['profile']
        key = profile_key(unit['path'], profile['compilerSha256'], profile['compilerFlags'])
        obj = root / object_relative(key)
        record = dict(source=unit['path'], module=unit['module'], mode=unit.get('mode', 'arm'),
                      object=object_relative(key), key=key,
                      compileProfile=dict(profile),
                      compilerFlags=list(profile['compilerFlags']))
        if obj.is_file() and obj.stat().st_size > 0:
            record.update(status='cached', objectSha256=digest(obj))
            return record
        attempts = []
        if unit['path'].endswith('.s'):
            attempts.append((str(assembler), ['-proc', ASSEMBLER_PROCESSOR]))
        flags = list(profile['compilerFlags'])
        if unit.get('mode') == 'thumb' and '-thumb' not in flags:
            flags.append('-thumb')
        if '-c' not in flags:
            flags.append('-c')
        attempts.append((str(compilers[profile['compilerSha256']]), flags))
        failure = None
        for tool, tool_flags in attempts:
            argv = [tool, *tool_flags, source.name, '-o', str(obj)]
            try:
                process = subprocess.run(argv, cwd=source.parent, env=env,
                                         capture_output=True, timeout=timeout)
            except (OSError, subprocess.TimeoutExpired) as error:
                failure = type(error).__name__ + ': ' + str(error)
                continue
            if process.returncode == 0 and obj.is_file() and obj.stat().st_size > 0:
                record.update(status='compiled', objectSha256=digest(obj), exitCode=0)
                return record
            failure = (process.stderr or process.stdout).decode('utf-8', 'replace')[-600:]
        record.update(status='compile-failed', error=failure)
        return record

    with short_paths(root) as (unused, short):
        # The compiler is a 32-bit process; very long repository paths are reached through
        # the drive-substituted view ``repo_build`` already provides.
        def build_short(unit):
            record = build(unit)
            return record

        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, min(int(jobs), 16))) as pool:
            records = list(pool.map(build_short, units))
    return records


# ---------------------------------------------------------------------------
# Ledger, symbols, plan


def load_ledger(private):
    """Address, size, mode, owning source and dependency names for every main function."""
    path = Path(private) / LEDGER_PATH
    if not path.is_file():
        raise WholeImageError('The address ledger is unavailable: ' + LEDGER_PATH)
    rows, dependencies = [], collections.Counter()
    with path.open(encoding='utf-8') as stream:
        for line in stream:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get('module') != MODULE:
                continue
            size = row.get('bytes')
            if type(size) is not int or size <= 0:
                continue
            # ``bytes`` is the ledger's own field name and is what ``pair_functions`` reads;
            # ``size`` is the same number under the name the rest of this module uses.
            # ``matchingBytes`` and the recorded profile are what the acceptance actually
            # achieved: a row whose matchingBytes is short of its size is a draft, not a
            # matched function, and a row whose flags differ from the source-unit rule needs
            # its own compile.
            rows.append(dict(address=hexint(row['address']), size=size, bytes=size,
                             symbol=row.get('symbol'), mode=row.get('mode') or 'arm',
                             source=(row.get('sourceUnit') or '').replace('\\', '/'),
                             matchingBytes=row.get('matchingBytes'),
                             compilerSha256=row.get('compilerSha256'),
                             compilerFlags=list(row.get('compilerFlags') or [])))
            for dependency in row.get('dependencies') or []:
                name = dependency.get('symbol')
                if not name:
                    continue
                target = dependency.get('target')
                if isinstance(target, str) and target.lower().startswith('0x'):
                    dependencies[(name, hexint(target))] += 1
                elif isinstance(target, int):
                    dependencies[(name, target)] += 1
    rows.sort(key=lambda item: item['address'])
    for left, right in zip(rows, rows[1:]):
        if left['address'] + left['size'] > right['address']:
            raise WholeImageError('The ledger has overlapping main functions at 0x%08x and 0x%08x'
                                  % (left['address'], right['address']))
    return rows, dependencies


def load_symbols(root):
    """The module symbol table: measured name -> address for functions, data and labels."""
    path = Path(root) / SYMBOLS_PATH
    if not path.is_file():
        return {}
    table = {}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        match = SYMBOL.match(line.strip())
        if not match:
            continue
        detail = match[3] or ''
        size = SYMBOL_SIZE.search(detail)
        table[match[1]] = dict(kind=match[2], address=hexint(match[4]),
                               size=hexint(size[1]) if size else None,
                               mode='thumb' if 'thumb' in detail else 'arm')
    return table


def plan_spans(root, units, records, ledger):
    """Decide what to place, what to stub and what to report as unusable.

    Pairing is the measurement's own pairing (``repo_build.pair_functions``) so the span
    this tool places is the span the ledger measured.
    """
    root = Path(root)
    # ``pair_functions`` reads a ledger row's address as the hexadecimal text the ledger
    # stores.  Give it text views and map every answer back to the integer form used here.
    def view(row):
        return dict(row, address='0x%08x' % row['address']) if row is not None else None

    def as_ledger_row(row):
        if row is None:
            return None
        if isinstance(row.get('address'), str):
            return dict(row, address=hexint(row['address']))
        return row

    by_address = {row['address']: view(row) for row in ledger}
    rows_by_source = collections.defaultdict(list)
    for row in ledger:
        rows_by_source[row['source']].append(row)
    placed, unpaired, inconsistent, failed = [], [], [], []
    for unit, record in zip(units, records):
        if record.get('status') not in ('compiled', 'cached'):
            failed.append(dict(source=unit['path'], status=record.get('status'),
                               error=record.get('error')))
            continue
        meta = read_elf(root / record['object'])
        functions = sorted(meta['functions'], key=lambda item: (item['section'], item['value']))
        if not functions:
            unpaired.append(dict(source=unit['path'], reason='object defines no function'))
            continue
        source_rows = sorted(rows_by_source.get(unit['path'], []), key=lambda row: row['address'])
        # Only a row the ledger declares fully matched, and whose compile profile this object
        # actually used, is a candidate for placement.  A draft row (matchingBytes short of
        # its size) is not a matched function; it stays a stub.
        profile = unit['profile']
        eligible, drafts = [], []
        for row in source_rows:
            if row['matchingBytes'] is not None and row['matchingBytes'] != row['size']:
                drafts.append(row)
                continue
            if row['compilerFlags']:
                same = (tuple(row['compilerFlags']) == tuple(profile['compilerFlags']) and
                        (not row['compilerSha256'] or
                         row['compilerSha256'] == profile['compilerSha256']))
                if not same:
                    drafts.append(row)
                    continue
            eligible.append(row)
        if drafts:
            unpaired.extend(dict(source=unit['path'], reason='not placed',
                                 address='0x%08x' % row['address'], symbol=row['symbol'],
                                 declared=row['size'], matching=row['matchingBytes'],
                                 recordedFlags=bool(row['compilerFlags']))
                            for row in drafts)
        proxies = [view(row) for row in eligible]
        entries = []
        for function, row in pair_functions(functions, proxies, by_address):
            row = as_ledger_row(row)
            if row is None:
                unpaired.append(dict(source=unit['path'], reason='no ledger row',
                                     symbol=function['name'], bytes=function['size']))
                continue
            entries.append(dict(function=function, row=row))
        if not entries:
            continue
        bases = {entry['row']['address'] - entry['function']['value'] for entry in entries}
        if len(bases) != 1:
            inconsistent.append(dict(source=unit['path'], reason='inconsistent bases',
                                     bases=sorted('0x%08x' % value for value in bases)))
            continue
        base = bases.pop()
        # The linker places the object's whole .text section, so the span the next address
        # must clear is the section size -- not the end of its last function symbol, which
        # can sit before trailing padding and would let the location counter move backward.
        text_sections = [section for section in meta['sections']
                         if section['name'] == '.text' and section['flags'] & EXECUTABLE]
        extent = sum(section['size'] for section in text_sections) or max(
            entry['function']['value'] + entry['function']['size'] for entry in entries)
        first = entries[0]['row']
        span = dict(address=base, extent=extent, object=Path(record['object']).name,
                    path=record['object'],
                    symbol=first['symbol'] or 'sub_%08x' % base,
                    size=max(entry['row']['size'] for entry in entries), mode=first['mode'],
                    source=unit['path'])
        mismatches = [dict(address='0x%08x' % entry['row']['address'],
                           declared=entry['row']['size'], compiled=entry['function']['size'])
                      for entry in entries if entry['function']['size'] != entry['row']['size']]
        if mismatches:
            span['sizeMismatch'] = mismatches
        placed.append(span)
    placed.sort(key=lambda span: span['address'])
    # A span whose compiled extent is longer than the ledger declared it would overwrite the
    # function behind it, so it is dropped before the overlap pass rather than taking its
    # neighbour down with it.
    dropped, kept = [], []
    for span in placed:
        if span.get('sizeMismatch'):
            dropped.append(dict(address='0x%08x' % span['address'], symbol=span['symbol'],
                                reason='compiled longer than declared',
                                detail=span['sizeMismatch']))
            continue
        kept.append(span)
    placed = kept
    # Absolute placement cannot express an overlap: keep the first span and report the rest.
    accepted, conflicts, cursor = [], [], None
    for span in placed:
        if cursor is not None and span['address'] < cursor:
            conflicts.append(dict(address='0x%08x' % span['address'], symbol=span['symbol'],
                                  source=span['source'], previousEnds='0x%08x' % cursor))
            continue
        accepted.append(span)
        cursor = span['address'] + span['extent']
    return accepted, unpaired, inconsistent, failed, conflicts, dropped


def coverage(layout, spans, ledger):
    """Bytes of the text window some reconstructed span covers, the holes, and the stubs."""
    text = layout['byName']['text']
    ordered = sorted(spans, key=lambda item: item['address'])
    cursor, holes, reconstructed = text['start'], [], 0
    for span in ordered:
        if span['address'] > cursor:
            holes.append(dict(start=cursor, end=span['address']))
        cursor = max(cursor, span['address'] + span['extent'])
        reconstructed += span['extent']
    if cursor < text['end']:
        holes.append(dict(start=cursor, end=text['end']))
    starts = [span['address'] for span in ordered]
    stub_rows, stub_bytes = 0, 0
    for row in ledger:
        index = bisect.bisect_right(starts, row['address']) - 1
        inside = (index >= 0 and
                  ordered[index]['address'] <= row['address'] <
                  ordered[index]['address'] + ordered[index]['extent'])
        if not inside:
            stub_rows += 1
            stub_bytes += row['size']
    return dict(reconstructedBytes=reconstructed, holes=holes,
                holeBytes=sum(hole['end'] - hole['start'] for hole in holes),
                stubRows=stub_rows, stubBytes=stub_bytes,
                ledgerRows=len(ledger), ledgerBytes=sum(row['size'] for row in ledger))


def section_budget(root, records, layout):
    """How many bytes the reconstructed objects put in the rodata and data windows."""
    totals = collections.Counter()
    for record in records:
        if record.get('status') not in ('compiled', 'cached'):
            continue
        for section in read_elf(Path(root) / record['object'])['sections']:
            name = section['name']
            if section['flags'] & EXECUTABLE or section['size'] == 0:
                continue
            if name.startswith('.rodata'):
                totals['rodata'] += section['size']
            elif name.startswith('.data'):
                totals['data'] += section['size']
    rodata, data = layout['byName']['rodata'], layout['byName']['data']
    budgets = dict(rodata=rodata['end'] - rodata['start'], data=data['end'] - data['start'])
    for name, total in totals.items():
        if total > budgets[name]:
            raise WholeImageError('Reconstructed objects need %d bytes of .%s but the module '
                                  'window is %d bytes' % (total, name, budgets[name]))
    return dict(objectBytes=dict(totals), windowBytes=budgets)


# ---------------------------------------------------------------------------
# Absolute symbol carrier


def render_absolute_symbols(symbols, ledger, dependencies, defined, entry):
    """Emit one assembly file that defines every measured symbol as an absolute symbol.

    A reconstructed object is placed at its measured address, but the names its relocations
    reference -- other functions, data objects, SDK entry points -- are not defined by any
    object.  The linker is given the measured address for each of them, taken from the
    module symbol table and the ledger, so the bytes it emits are the bytes the original
    link produced.
    """
    resolved = {}

    def admit(name, address, origin):
        if not name or not IDENTIFIER.match(name) or name.startswith('.'):
            return
        if name in defined:
            return
        previous = resolved.get(name)
        if previous is None:
            resolved[name] = dict(address=address, origin=origin)
        elif previous['address'] != address:
            previous.setdefault('conflicts', []).append(dict(address='0x%08x' % address,
                                                            origin=origin))

    for name, row in symbols.items():
        admit(name, row['address'], 'symbols.txt')
    for row in ledger:
        if row['symbol']:
            admit(row['symbol'], row['address'], 'ledger')
    for (name, address) in sorted(dependencies):
        admit(name, address, 'ledger.dependencies')
        match = ADDRESS_SUFFIX.search(name)
        if match:
            admit(name, int(match.group(1), 16), 'ledger.dependencies.name')
    conflicts = [dict(symbol=name, address='0x%08x' % row['address'], conflicts=row['conflicts'])
                 for name, row in sorted(resolved.items()) if row.get('conflicts')]
    lines = ['# GENERATED by public_tools/whole_image_link.py -- absolute symbol carrier.',
             '#',
             '# The whole-image link places every reconstructed object at its measured address,',
             '# so every name a relocation can reference must resolve to its measured address',
             '# too.  %s gives the address of every function,' % SYMBOLS_PATH,
             '# data object and label in the module; the ledger adds the relocation dependency',
             '# names the sources actually spell.  `name = 0xADDR` is an absolute symbol in',
             '# the Metrowerks assembler and costs no image bytes; `.global` is what makes it',
             '# visible to the linker rather than local to this object.',
             '',
             '# entry point: mwldarm defaults to __startup',
             '.global __startup',
             '__startup = 0x%08x' % entry,
             '']
    for name, row in sorted(resolved.items()):
        lines.append('.global ' + name)
        lines.append('%-40s = 0x%08x' % (name, row['address']))
    return '\n'.join(lines) + '\n', len(resolved), conflicts


# ---------------------------------------------------------------------------
# Link and diff


def run_link(out, linker, lcf, objects, extra):
    """Invoke the pinned linker through a response file; the object list outgrows a command line.

    The working directory is the build directory: the command file can only name an input
    object by a bare file name, so objects, the absolute symbol carrier and the region
    output file are all named relative to it.
    """
    work_dir = Path(out)
    response = work_dir / 'objects.rsp'
    argv = ['-nostdlib', '-nodeadstrip', '-msgstyle', 'gcc', '-maxerrors', '0',
            '-o', 'arm9.elf', 'arm9.lcf', 'abs.o', *extra, *objects]
    response.write_text('\n'.join(argv) + '\n', encoding='utf-8')
    process = subprocess.run([str(linker), '@objects.rsp'], cwd=str(work_dir),
                             capture_output=True, env=dict(os.environ))
    return process.returncode, (process.stdout + b'\n' + process.stderr).decode('utf-8', 'replace')


def undefined_symbols(text):
    names = []
    for line in text.splitlines():
        match = re.search(r'Undefined\s*:\s*"?([A-Za-z_$][A-Za-z0-9_$.]*)"?', line)
        if match:
            names.append(match.group(1))
    return sorted(set(names))


def global_definitions(elf_bytes):
    """The names an ELF object defines globally in an allocated section.

    Debug sections are excluded on purpose: ``-sym on`` gives every object the same global
    ``.dwarf_type.int``/``.dwarf_typedef.u32`` symbols, which are not part of the image and
    are not a link conflict.  Only symbols defined in a section with ``SHF_ALLOC`` can own a
    byte of the module.
    """
    if elf_bytes[:7] != b'\x7fELF\x01\x01\x01':
        raise WholeImageError('Not an ARM ELF32 object')
    header = struct.unpack_from('<16sHHIIIIIHHHHHH', elf_bytes)
    shentsize, shnum = header[11], header[12]
    sections = [struct.unpack_from('<IIIIIIIIII', elf_bytes, header[6] + shentsize * index)
                for index in range(shnum)]
    allocated = {index for index, section in enumerate(sections) if section[2] & ALLOCATABLE}
    names = set()
    for section in sections:
        if section[1] != 2 or section[6] >= len(sections):
            continue
        strings = sections[section[6]]
        blob = elf_bytes[strings[4]:strings[4] + strings[5]]
        for offset in range(0, section[5], 16):
            name_at, value, size, info, unused, shndx = struct.unpack_from(
                '<IIIBBH', elf_bytes, section[4] + offset)
            if shndx not in allocated or (info >> 4) not in (1, 2):
                continue
            end = blob.find(b'\0', name_at)
            if end < 0:
                continue
            name = blob[name_at:end].decode('utf-8', 'replace')
            if name:
                names.add(name)
    return names


def undefined_names(elf_bytes):
    """The global names an object references but does not define."""
    header = struct.unpack_from('<16sHHIIIIIHHHHHH', elf_bytes)
    shentsize, shnum = header[11], header[12]
    sections = [struct.unpack_from('<IIIIIIIIII', elf_bytes, header[6] + shentsize * index)
                for index in range(shnum)]
    names = set()
    for section in sections:
        if section[1] != 2 or section[6] >= len(sections):
            continue
        strings = sections[section[6]]
        blob = elf_bytes[strings[4]:strings[4] + strings[5]]
        for offset in range(0, section[5], 16):
            name_at, value, size, info, unused, shndx = struct.unpack_from(
                '<IIIBBH', elf_bytes, section[4] + offset)
            if shndx != 0 or (info >> 4) not in (1, 2):
                continue
            end = blob.find(b'\0', name_at)
            if end < 0:
                continue
            name = blob[name_at:end].decode('utf-8', 'replace')
            if name:
                names.add(name)
    return names


def resolvable(name, symbols, defined):
    """Whether the carrier or a placed object can give this name an address."""
    return name in defined or name in symbols or ADDRESS_SUFFIX.search(name) is not None


def drop_unresolved(root, spans, symbols, defined):
    """Remove placements whose object still references a name nothing can resolve.

    The module symbol table and the ledger name almost every external a source spells.  A
    handful are not named anywhere public -- NitroSDK 3D lookups (``NNS_G3dGetResDataByName``),
    the Metrowerks 64-bit helpers (``_ll_sdiv``, ``_ll_mod``) and a few helpers defined in a
    source file that is not placed.  A function that needs one of those cannot be linked; it
    is dropped from the placement (and so appears in the diff as a stub) rather than faking
    an address.
    """
    kept, dropped = [], []
    for span in spans:
        missing = sorted(name for name in read_elf(Path(root) / span['path'])['undefined']
                         if not resolvable(name, symbols, defined))
        if missing:
            dropped.append(dict(address='0x%08x' % span['address'], symbol=span['symbol'],
                                source=span['source'], reason='unresolved external symbol',
                                symbols=missing[:8]))
            continue
        kept.append(span)
    return kept, dropped


def resolve_duplicate_symbols(root, spans):
    """Drop placements whose object re-defines a global an earlier placement already owns.

    Two source files can both declare the same global (usually a data object in the
    unreconstructed window).  The linker refuses the duplicate, and only one address can be
    the measured one, so the later placement is dropped and reported instead of silently
    winning.
    """
    kept, dropped, owned = [], [], {}
    for span in spans:
        names = read_elf(Path(root) / span['path'])['globals']
        clash = sorted(name for name in names if name in owned)
        if clash:
            dropped.append(dict(address='0x%08x' % span['address'], symbol=span['symbol'],
                                source=span['source'], reason='duplicate global symbol',
                                symbols=clash[:8], firstOwner='0x%08x' % owned[clash[0]]))
            continue
        kept.append(span)
        for name in names:
            owned[name] = span['address']
    return kept, dropped, owned


def linked_symbols(elf_bytes, allocated_only=True):
    """Where every symbol that owns image bytes landed in an ELF32 image or object.

    For an *object*, only symbols in a section with ``SHF_ALLOC`` count: ``-sym on`` adds
    debug symbols named after the function into non-allocated sections.  For the *link
    product* the flag test cannot be used -- the Metrowerks LCF region section carries a
    vendor flag instead of ``SHF_ALLOC`` -- so the debug sections are skipped by name.
    """
    header = struct.unpack_from('<16sHHIIIIIHHHHHH', elf_bytes)
    shentsize, shnum, shstrndx = header[11], header[12], header[13]
    sections = [struct.unpack_from('<IIIIIIIIII', elf_bytes, header[6] + shentsize * index)
                for index in range(shnum)]
    names = elf_bytes[sections[shstrndx][4]:sections[shstrndx][4] + sections[shstrndx][5]]

    def section_name(index):
        end = names.find(b'\0', sections[index][0])
        return names[sections[index][0]:end].decode('utf-8', 'replace')

    if allocated_only:
        allowed = {index for index, section in enumerate(sections) if section[2] & ALLOCATABLE}
    else:
        allowed = {index for index in range(shnum) if not section_name(index).startswith('.dwarf')}
    result = {}
    for section in sections:
        if section[1] != 2 or section[6] >= len(sections):
            continue
        strings = sections[section[6]]
        blob = elf_bytes[strings[4]:strings[4] + strings[5]]
        for offset in range(0, section[5], 16):
            name_at, value, size, info, unused, shndx = struct.unpack_from(
                '<IIIBBH', elf_bytes, section[4] + offset)
            if shndx not in allowed:
                continue
            end = blob.find(b'\0', name_at)
            if end < 0:
                continue
            name = blob[name_at:end].decode('utf-8', 'replace')
            if name:
                result[name] = value
    return result


def diff_image(produced, original, layout, spans, ledger):
    """Compare the linked image with the extracted one and attribute every difference."""
    text = layout['byName']['text']
    if len(produced) != len(original):
        raise WholeImageError('Linked image is %d bytes, the module declares %d'
                              % (len(produced), len(original)))
    base = text['start']
    spans = sorted(spans, key=lambda item: item['address'])
    rows = sorted(ledger, key=lambda item: item['address'])
    span_starts = [span['address'] for span in spans]
    row_starts = [row['address'] for row in rows]
    boundaries = sorted(set(span_starts) | set(row_starts) | {text['start'], text['end']})

    def span_at(address):
        index = bisect.bisect_right(span_starts, address) - 1
        if index >= 0 and spans[index]['address'] <= address < spans[index]['address'] + spans[index]['extent']:
            return spans[index]
        return None

    def row_at(address):
        index = bisect.bisect_right(row_starts, address) - 1
        if index >= 0 and rows[index]['address'] <= address < rows[index]['address'] + rows[index]['size']:
            return rows[index]
        return None

    differing = [index for index in range(len(original)) if produced[index] != original[index]]
    buckets = collections.Counter()
    per_function = {}
    gaps = []
    ranges = 0
    index = 0
    while index < len(differing):
        start = differing[index]
        end = start + 1
        index += 1
        while index < len(differing) and differing[index] == end:
            end += 1
            index += 1
        ranges += 1
        cursor = start
        while cursor < end:
            address = base + cursor
            span, row = span_at(address), row_at(address)
            limit = end
            position = bisect.bisect_right(boundaries, address)
            if position < len(boundaries):
                limit = min(limit, boundaries[position] - base)
            # A chunk never crosses the end of the function, span or hole it started in:
            # otherwise the bytes behind a short function are attributed to it and the
            # per-function report inflates.
            if row is not None:
                limit = min(limit, row['address'] + row['size'] - base)
            if span is not None:
                limit = min(limit, span['address'] + span['extent'] - base)
            if limit <= cursor:
                limit = cursor + 1
            count = limit - cursor
            if span is not None:
                buckets['reconstructed'] += count
                key = row['address'] if row is not None else span['address']
                entry = per_function.setdefault(key, dict(
                    address=key,
                    symbol=row['symbol'] if row is not None else span['symbol'],
                    mode=row['mode'] if row is not None else span['mode'],
                    size=row['size'] if row is not None else span['size'],
                    source=row['source'] if row is not None else span['source'], differing=0))
                entry['differing'] += count
            elif row is not None:
                buckets['stub'] += count
            elif address >= text['end']:
                # .rodata, .ctor and .data are not reconstructed at all yet; the window is
                # reported separately so a text hole is never confused with a data window.
                buckets['dataWindow'] += count
            else:
                buckets['gap'] += count
                gaps.append(dict(start='0x%08x' % address, end='0x%08x' % (address + count)))
            cursor = limit
    mismatched = sorted((entry for entry in per_function.values() if entry['differing']),
                        key=lambda entry: (-entry['differing'], entry['address']))
    # A span reproduces when its own placed bytes equal the image's bytes, judged span by
    # span so the answer does not depend on how the ledger happens to split a block.
    reproduced = []
    for span in spans:
        start = span['address'] - base
        end = start + span['extent']
        if produced[start:end] == original[start:end]:
            reproduced.append(dict(address='0x%08x' % span['address'], symbol=span['symbol'],
                                   bytes=span['extent'], source=span['source']))
    return dict(totalBytes=len(original), differingBytes=len(differing), differingRanges=ranges,
                reproduced=reproduced,
                reproducedBytes=sum(item['bytes'] for item in reproduced),
                reproducedSpans=len(reproduced),
                reconstructedDifferingBytes=buckets['reconstructed'],
                stubDifferingBytes=buckets['stub'], gapDifferingBytes=buckets['gap'],
                dataWindowDifferingBytes=buckets['dataWindow'],
                mismatchedFunctions=len(mismatched),
                mismatched=[dict(address='0x%08x' % entry['address'], symbol=entry['symbol'],
                                 mode=entry['mode'], size=entry['size'], source=entry['source'],
                                 differing=entry['differing']) for entry in mismatched[:200]],
                gapsOutsideFunctions=gaps[:200])


# ---------------------------------------------------------------------------
# Pipeline


def install_inputs(root, bundle):
    """Materialise the pinned private-input bundle into the checkout.

    This is the same mechanism the authored-code build uses: CI checks out
    ``trevorWieland/dqmj2-pro-inputs`` at a pinned revision and
    ``build_bytematch.install_bundle`` unpacks ``extract/``, ``ledger/`` and ``tools/`` into
    the checkout, refusing any conflict with a tracked file.  Nothing private is committed.
    """
    if not bundle:
        return dict(status='not-requested')
    candidate = Path(root) / bundle if not Path(bundle).is_absolute() else Path(bundle)
    if not candidate.is_dir():
        return dict(status='absent', path=str(bundle))
    from build_bytematch import install_bundle
    return dict(status='installed', **install_bundle(Path(root), candidate))


def inputs_present(root):
    """The two private inputs the gate cannot work without."""
    return (Path(root) / IMAGE_PATH).is_file() and (Path(root) / LEDGER_PATH).is_file()


def layout_report(root):
    """Validate the section table and print the derived image geometry (no private inputs)."""
    layout = load_layout(root)
    expected, notes = check_header(root, layout)
    text, data, bss = layout['byName']['text'], layout['byName']['data'], layout['byName']['bss']
    return dict(status='layout-ok', source=DELINKS_PATH,
                sections=[dict(name=section['name'], start='0x%08x' % section['start'],
                               end='0x%08x' % section['end'],
                               bytes=section['end'] - section['start'],
                               kind=section['kind'], align=section['align'])
                          for section in layout['sections']],
                base='0x%08x' % expected['base'], imageBytes=expected['bytes'],
                textBytes=text['end'] - text['start'],
                rodataBytes=layout['byName']['rodata']['end'] - layout['byName']['rodata']['start'],
                ctorBytes=layout['byName']['ctor']['end'] - layout['byName']['ctor']['start'],
                dataBytes=data['end'] - data['start'], bssBytes=bss['end'] - bss['start'],
                headerChecks=notes)


def read_baseline(root):
    path = Path(root) / BASELINE_PATH
    if not path.is_file():
        return None
    document = json.loads(path.read_text(encoding='utf-8'))
    if document.get('schemaVersion') != 1:
        raise WholeImageError('Unsupported baseline schema in ' + BASELINE_PATH)
    return document


def compare_baseline(baseline, diff, spans):
    """Which functions the baseline records as reproducing no longer do.

    The baseline is the set of functions this gate has already proved byte for byte.  It is
    regenerated with ``--emit-baseline`` and committed; CI fails when a function leaves the
    set, because losing a match is a regression even if the image as a whole still links.
    """
    placed = {span['symbol']: span for span in spans}
    reproduced = {item['symbol'] for item in diff['reproduced']}
    regressions = []
    for item in baseline.get('reproduced', []):
        # The committed form is a compact triple; a mapping is accepted too.
        address, symbol = (item[0], item[1]) if isinstance(item, list) else (item['address'], item['symbol'])
        span = placed.get(symbol)
        if span is None:
            regressions.append(dict(symbol=symbol, address=address, reason='not placed'))
        elif '0x%08x' % span['address'] != address:
            regressions.append(dict(symbol=symbol, address=address, reason='displaced',
                                    now='0x%08x' % span['address']))
        elif symbol not in reproduced:
            regressions.append(dict(symbol=symbol, address=address, reason='differs'))
    return regressions


def emit_baseline(root, diff, provenance):
    path = Path(root) / BASELINE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    document = dict(schemaVersion=1, generatedTimeNs=time.time_ns(), module=MODULE,
                    imageSha256=provenance['imageSha256'],
                    delinksSha256=provenance['delinksSha256'],
                    builder='public_tools/whole_image_link.py --emit-baseline',
                    note='Every function listed here links to the extracted bytes exactly. '
                         'The gate fails when one of them leaves the set.',
                    reproducedBytes=diff['reproducedBytes'],
                    reproducedSpans=len(diff['reproduced']),
                    reproduced=[[item['address'], item['symbol'], item['bytes']]
                                for item in diff['reproduced']])
    path.write_text(json.dumps(document, indent=0) + '\n', encoding='utf-8')
    return dict(status='baseline-written', path=BASELINE_PATH,
                reproducedBytes=diff['reproducedBytes'], reproduced=len(diff['reproduced']))


def emit(root, out, jobs, emit_lcf, check_lcf, region_file, limit, write_baseline=False):
    root = Path(root)
    config = load_config(root)
    layout = load_layout(root)
    expected, header_notes = check_header(root, layout)
    delinks_sha = digest(root / DELINKS_PATH)
    compiled, assembly = main_units(root, config)
    if limit:
        compiled, assembly = compiled[:limit], assembly[:limit]
    compilers, assembler, linker, license_file = toolchain_paths(root, config)
    if license_file:
        os.environ['LM_LICENSE_FILE'] = str(license_file)
    raw_units = compiled + assembly
    ledger, dependencies = load_ledger(root)
    # The compile profile comes from the ledger row, not from the directory rule: a source is
    # sometimes accepted under flags the rule does not carry, and recompiling it with the
    # rule's flags produces different bytes.
    profiles = unit_profiles(raw_units, ledger)
    units = [dict(unit, profile=profiles[unit['path']]) for unit in raw_units]
    note('compiling %d units' % len(units))
    records = compile_units(root, units, compilers, assembler, out, jobs)
    symbols = load_symbols(root)
    note('planning placements')
    note('planning placements')
    spans, unpaired, inconsistent, failed, conflicts, dropped = plan_spans(root, units, records, ledger)
    note('planned %d spans' % len(spans))
    note('planned %d spans' % len(spans))
    spans, duplicate_drops, owned = resolve_duplicate_symbols(root, spans)
    dropped.extend(duplicate_drops)
    note('dropping placements with unresolvable externals')
    spans, unresolved_drops = drop_unresolved(root, spans, symbols, set(owned))
    note('placed %d spans, dropped %d' % (len(spans), len(dropped) + len(unresolved_drops)))
    dropped.extend(unresolved_drops)
    relaxed = []
    for span in spans:
        changed = relax_object_alignment(root / span['path'], natural_alignment(span['address']))
        if changed:
            relaxed.append(dict(symbol=span['symbol'], address='0x%08x' % span['address'],
                                changed=changed))
    cover = coverage(layout, spans, ledger)
    budget = section_budget(root, records, layout)
    lcf_text = render_lcf(layout, spans, region_file, dict(delinksSha256=delinks_sha))
    committed = root / LCF_PATH
    if check_lcf:
        if not committed.is_file():
            raise WholeImageError('The committed linker command file is missing: ' + LCF_PATH)
        if committed.read_text(encoding='utf-8').replace('\r\n', '\n') != lcf_text:
            raise WholeImageError('The committed linker command file is stale: regenerate '
                                  + LCF_PATH + ' with --emit-lcf')
        return dict(status='lcf-current', path=LCF_PATH, spans=len(spans))
    if emit_lcf:
        committed.parent.mkdir(parents=True, exist_ok=True)
        committed.write_text(lcf_text, encoding='utf-8')
        return dict(status='lcf-written', path=LCF_PATH, spans=len(spans), bytes=len(lcf_text),
                    reconstructedBytes=cover['reconstructedBytes'], holeBytes=cover['holeBytes'],
                    stubRows=cover['stubRows'], ledgerRows=cover['ledgerRows'])
    out_dir = root / out
    out_dir.mkdir(parents=True, exist_ok=True)
    lcf = out_dir / 'arm9.lcf'
    lcf.write_text(lcf_text, encoding='utf-8')
    (out_dir / 'plan.json').write_text(json.dumps(dict(
        spans=[dict(address='0x%08x' % span['address'], bytes=span['extent'],
                    symbol=span['symbol'], mode=span['mode'], source=span['source'],
                    object=span['object']) for span in spans],
        relaxed=relaxed), indent=2) + '\n', encoding='utf-8')
    # Every global an already-placed object defines is off limits for the carrier: defining
    # it twice is a "Multiply-defined" error.  ``owned`` comes from the duplicate pass, so it
    # covers data symbols as well as code.
    defined = set(owned)
    note('writing the absolute symbol carrier')
    note('writing the absolute symbol carrier')
    absolute, symbol_rows, symbol_conflicts = render_absolute_symbols(
        symbols, ledger, dependencies, defined, layout['byName']['text']['start'])
    (out_dir / 'abs.s').write_text(absolute, encoding='utf-8')
    process = subprocess.run([str(assembler), '-proc', ASSEMBLER_PROCESSOR, 'abs.s', '-o', 'abs.o'],
                             cwd=str(out_dir), capture_output=True)
    if process.returncode != 0 or not (out_dir / 'abs.o').is_file():
        raise WholeImageError('Assembling the absolute symbol carrier failed: '
                              + (process.stderr or process.stdout).decode('utf-8', 'replace')[-600:])
    objects = [span['object'] for span in spans]
    note('linking %d objects' % len(objects))
    code, text = run_link(out_dir, linker, 'arm9.lcf', objects, [])
    note('link exit %d' % code)
    attempts = 0
    # The module symbol table plus the ledger covers almost every name a source spells; the
    # rest are address-encoded (`native_fn_0200e46c`) and are recovered from the name itself.
    # Each round accumulates, so a symbol resolved on round two survives round three.
    recovered = {}
    while code != 0 and attempts < 6:
        missing = undefined_symbols(text)
        added = 0
        for name in missing:
            if name in recovered:
                continue
            row = symbols.get(name)
            if row is not None:
                recovered[name] = row['address']
                added += 1
                continue
            match = ADDRESS_SUFFIX.search(name)
            if match:
                recovered[name] = int(match.group(1), 16)
                added += 1
        if not added:
            break
        extra = []
        for name, address in sorted(recovered.items()):
            extra.append('.global ' + name)
            extra.append('%-40s = 0x%08x' % (name, address))
        (out_dir / 'abs.s').write_text(absolute + '\n# resolved from link diagnostics\n'
                                       + '\n'.join(extra) + '\n', encoding='utf-8')
        process = subprocess.run([str(assembler), '-proc', ASSEMBLER_PROCESSOR, 'abs.s', '-o', 'abs.o'],
                                 cwd=str(out_dir), capture_output=True)
        if process.returncode != 0:
            raise WholeImageError('Assembling the resolved symbols failed: '
                                  + (process.stderr or process.stdout).decode('utf-8', 'replace')[-600:])
        note('linking %d objects (retry %d)' % (len(objects), attempts + 1))
        code, text = run_link(out_dir, linker, 'arm9.lcf', objects, [])
        note('link exit %d' % code)
        attempts += 1
    region = out_dir / region_file
    result = dict(
        schemaVersion=1, generatedTimeNs=time.time_ns(), module=MODULE,
        status='link-passed' if code == 0 else 'link-failed',
        layout=dict(source=DELINKS_PATH,
                    sections=[dict(name=section['name'], start='0x%08x' % section['start'],
                                   end='0x%08x' % section['end'],
                                   bytes=section['end'] - section['start'],
                                   kind=section['kind'], align=section['align'])
                              for section in layout['sections']],
                    base='0x%08x' % expected['base'], imageBytes=expected['bytes'],
                    headerChecks=header_notes),
        link=dict(exitCode=code, attempts=attempts + 1, objects=len(objects),
                  regionFile=region_file,
                  regionFileBytes=region.stat().st_size if region.is_file() else 0,
                  expectedBytes=expected['bytes'],
                  sizeMatches=(region.is_file() and region.stat().st_size == expected['bytes']),
                  absoluteSymbols=symbol_rows, symbolConflicts=len(symbol_conflicts),
                  outputTail=text[-4000:]),
        sources=dict(compiled=len(compiled), assembly=len(assembly),
                     compiledOk=sum(1 for record in records
                                    if record.get('status') in ('compiled', 'cached')),
                     failed=len(failed), placedSpans=len(spans), unpaired=len(unpaired),
                     unpairedDetail=unpaired[:80], inconsistentUnits=inconsistent[:40],
                     placementConflicts=conflicts[:40], droppedSpans=dropped[:40],
                     sizeMismatchSpans=sum(1 for span in spans if span.get('sizeMismatch')), relaxedObjects=len(relaxed),
                     sizeMismatchDetail=[dict(symbol=span['symbol'], detail=span['sizeMismatch'])
                                         for span in spans if span.get('sizeMismatch')][:40],
                     objectSectionBytes=budget['objectBytes'],
                     windowBytes=budget['windowBytes']),
        text=dict(region='0x%08x..0x%08x' % (layout['byName']['text']['start'],
                                             layout['byName']['text']['end']),
                  reconstructedBytes=cover['reconstructedBytes'], holeBytes=cover['holeBytes'],
                  holes=len(cover['holes']), stubRows=cover['stubRows'],
                  stubBytes=cover['stubBytes'], ledgerRows=cover['ledgerRows'],
                  ledgerBytes=cover['ledgerBytes']),
        failures=failed[:40],
    )
    if code != 0:
        (out_dir / 'link.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        raise WholeImageError('The whole-image link failed; see %s'
                              % (out_dir / 'link.json').relative_to(root).as_posix())
    note('diffing the linked image')
    note('diffing the linked image')
    original = (root / IMAGE_PATH).read_bytes()
    produced = region.read_bytes()
    # Placement proof: every span's symbol must sit at the measured address in the link product.
    placed = linked_symbols((out_dir / 'arm9.elf').read_bytes(), allocated_only=False)
    displaced = [dict(symbol=span['symbol'], expected='0x%08x' % span['address'],
                      linked='0x%08x' % placed[span['symbol']])
                 for span in spans
                 if span['symbol'] in placed and placed[span['symbol']] != span['address']]
    diff = diff_image(produced, original, layout, spans, ledger)
    result['diff'] = diff
    result['placement'] = dict(checked=sum(1 for span in spans if span['symbol'] in placed),
                               missing=sum(1 for span in spans if span['symbol'] not in placed),
                               displaced=displaced[:80], displacedCount=len(displaced))
    result['inputs'] = dict(
        image=dict(path=IMAGE_PATH, bytes=len(original), sha256=digest(root / IMAGE_PATH)),
        ledger=dict(path=LEDGER_PATH, sha256=digest(root / LEDGER_PATH), rows=len(ledger)),
        symbols=dict(path=SYMBOLS_PATH, names=len(symbols)),
        delinks=dict(path=DELINKS_PATH, sha256=delinks_sha),
        config=dict(path=CONFIG, sha256=config_digest(root)),
    )
    rom = root / ROM_PATH
    rom_matches = None
    if rom.is_file():
        observed = digest(rom)
        rom_matches = observed == ROM_SHA256 and rom.stat().st_size == ROM_BYTES
        result['inputs']['rom'] = dict(path=ROM_PATH, bytes=rom.stat().st_size, sha256=observed,
                                       expectedSha256=ROM_SHA256, expectedBytes=ROM_BYTES,
                                       matches=rom_matches)
    gate = dict(
        sizeMatches=result['link']['sizeMatches'],
        noDisplacedFunctions=not displaced,
    )
    if rom_matches is not None:
        # The ROM the module was extracted from is part of the identity of the gate's input.
        gate['romIdentityMatches'] = rom_matches
    baseline = read_baseline(root)
    residual = dict(reproducedBytes=diff['reproducedBytes'],
                    reproducedSpans=diff['reproducedSpans'],
                    placedSpans=len(spans),
                    nonReproducingSpans=diff['mismatchedFunctions'],
                    nonReproducingBytes=diff['reconstructedDifferingBytes'])
    if baseline is not None:
        # The gate proper: every function the baseline records as reproducing must keep
        # reproducing, and the reproduced byte count must not fall.
        regressions = compare_baseline(baseline, diff, spans)
        gate['noBaselineRegressions'] = not regressions
        gate['reproducedBytesAtLeastBaseline'] = (
            diff['reproducedBytes'] >= baseline.get('reproducedBytes', 0))
        result['baseline'] = dict(path=BASELINE_PATH, status='compared',
                                  reproducedBytes=baseline.get('reproducedBytes'),
                                  reproducedSpans=baseline.get('reproducedSpans'),
                                  regressions=regressions[:200], regressionCount=len(regressions))
    else:
        gate['noReconstructedDifferences'] = diff['reconstructedDifferingBytes'] == 0
        result['baseline'] = dict(path=BASELINE_PATH, status='absent')
    result['residual'] = residual
    result['gate'] = gate
    result['status'] = 'gate-passed' if all(gate.values()) else 'gate-failed'
    (out_dir / 'summary.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    if write_baseline:
        result['baselineWritten'] = emit_baseline(
            root, diff, dict(imageSha256=result['inputs']['image']['sha256'],
                             delinksSha256=delinks_sha))
    return result


def main():
    parser = argparse.ArgumentParser(description='Link the whole reconstructed ARM9 image and diff it.')
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--out', default='build/whole-image')
    parser.add_argument('--region-file', default='arm9.bin')
    parser.add_argument('--jobs', type=int, default=8)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--emit-lcf', action='store_true')
    parser.add_argument('--check-lcf', action='store_true')
    parser.add_argument('--emit-baseline', dest='emit_baseline_doc', action='store_true',
                        help='refresh ports/recompile/arm9-baseline.json from this link')
    parser.add_argument('--check-layout', action='store_true',
                        help='validate the section table only; needs no private inputs')
    parser.add_argument('--input-bundle', default=None,
                        help='install the pinned private-input bundle from this path first')
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.check_layout:
            print(json.dumps(layout_report(root), indent=2))
            return 0
        install = install_inputs(root, args.input_bundle)
        if not inputs_present(root):
            # The gate cannot run without the extracted module image and the address ledger.
            # Both arrive through the pinned private-input bundle, never as a commit, so an
            # absent bundle is a skip rather than a failure.
            print(json.dumps(dict(status='skipped-missing-inputs', install=install,
                                  required=[IMAGE_PATH, LEDGER_PATH]), indent=2))
            return 0
        result = emit(root, args.out, args.jobs, args.emit_lcf, args.check_lcf,
                      args.region_file, args.limit, args.emit_baseline_doc)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, 'whole-image link: ' + str(error) + '\n')
    printable = {key: value for key, value in result.items()
                 if key in ('status', 'text', 'diff', 'gate', 'link', 'sources', 'placement',
                            'spans', 'bytes', 'reconstructedBytes', 'holeBytes', 'stubRows',
                            'ledgerRows', 'path')}
    print(json.dumps(printable, indent=2))
    return 0 if result.get('status') in ('lcf-written', 'lcf-current', 'gate-passed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
