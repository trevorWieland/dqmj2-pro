#!/usr/bin/env python3
"""Build decomp-permuter workspaces for measured rows, run the search, accept a hit.

The hand-matching loop stalls on one class of row: the C is reachable and compiles to
the exact measured size, but mwccarm picks a different register, stack slot or branch
form. `ops/form_search.py` enumerates hand-written template variants; `ops/permute.py`
hill-climbs over a fixed edit catalogue. Neither reaches the space decomp-permuter's
AST randomizer covers.

This module is the project adapter for the real thing
(github.com/simonlindholm/decomp-permuter, pinned commit
``8556c81d80d1c1af98a858c8f4dc951357f29139``, acquired by
``acquire_decomp_permuter_20261101.py``, never vendored into git). decomp-permuter's
interface is a directory holding four things, and this tool generates all four from a
ledger address:

``base.c``       the current best-known source (``--src``, or a copy of ``--src`` taken
                 from an existing file on disk),
``target.o``     the ORIGINAL image bytes for the row, in a real mwccarm object so the
                 relocation table survives, with every relocation slot zeroed,
``compile.sh``   the pinned mwccarm build with the row's exact flags and ``-thumb``,
``settings.toml`` ``func_name``, ``compiler_type = "mwcc"``, and an ``objdump_command``
                 pointing at :mod:`ops.mwcc_objdump` (Capstone, because no GNU-style ARM
                 objdump exists here).

Why ``target.o`` is derived from ``base.o`` instead of being built from scratch: the
relocation table of the base compile names the externals exactly as the C source names
them, at the same offsets the original used (the premise of a permuter row is that the
structure already matches). So ``target.o`` is the base object with ``.text`` rewritten
to the image slice and the relocation slots zeroed. That keeps both sides of the diff
on identical relocation text, which is what makes a score of 0 meaningful.

    python ops/permuter.py build --module ov006 --address 0x02203EBC \\
        --src ops/compiler_specs/02203ebc.c
    python ops/permuter.py probe work/permuter/ov006_02203ebc
    python ops/permuter.py run work/permuter/ov006_02203ebc --timeout 300
    python ops/verify_permuter.py work/permuter/ov006_02203ebc --source best.c

A permuter score is NOT acceptance. See ``docs/authoring/permuter.md``: only
``ops/verify_permuter.py`` (project compile + relocation + byte compare + negative
controls) may promote a result.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from elftools.elf.elffile import ELFFile  # noqa: E402

PERMUTER_REPOSITORY = 'https://github.com/simonlindholm/decomp-permuter.git'
PERMUTER_PIN = '8556c81d80d1c1af98a858c8f4dc951357f29139'
PERMUTER_ACQUIRE = 'acquire_decomp_permuter_20261101.py'
WORKSPACES = ROOT / 'work/permuter'

# The pinned build is what the ledger's accepted rows reproduce under (see
# ops/compiler_matrix.py: every other installed build loses on more rows).
DEFAULT_COMPILER = 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
LICENSE = 'tools/mwccarm/mwccarm/license.dat'

# Passes that move register allocation without changing the shape of the function:
# operand order, declaration order, temporary introduction, and signedness. This row
# class is exactly "same instructions, different registers", so these are weighted up
# over the structural rewrites that would change the instruction count.
REGALLOC_WEIGHTS = {
    'perm_temp_for_expr': 100,
    'perm_commutative': 25,
    'perm_inequalities': 15,
    'perm_reorder_decls': 20,
    'perm_reorder_stmts': 15,
    'perm_cast_simple': 20,
    'perm_refer_to_var': 15,
    'perm_expand_expr': 20,
}

FUNCTION = re.compile(
    r'^(?![ \t]*(?:if|for|while|switch|return|else)\b)'
    r'[ \t]*(?:[A-Za-z_][A-Za-z0-9_]*(?:[ \t]+|[ \t]*\*[ \t]*))+'
    r'(?P<name>[A-Za-z_][A-Za-z0-9_]*)[ \t]*\([^;{]*\)[ \t]*\n?[ \t]*\{',
    re.M)
QUOTED_INCLUDE = re.compile(r'^[ \t]*#[ \t]*include[ \t]*"([^"]+)"', re.M)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def digest_file(path):
    return sha256(Path(path).read_bytes())


# ---------------------------------------------------------------- project inputs

def module_info(root, module):
    """(image bytes, load address, image path) for a module named in the build config."""
    config = json.loads((root / 'config/source_units.json').read_text(encoding='utf-8-sig'))
    try:
        info = config['modules'][module]
    except KeyError:
        raise SystemExit(f'unknown module {module!r}; known: '
                         + ', '.join(sorted(config['modules'])))
    path = root / info['originalImage']
    if not path.is_file():
        raise SystemExit(f'module image is missing: {path} (extract/ is not committed)')
    return path.read_bytes(), int(str(info['loadAddressBase']), 0), path


def ledger_row(root, module, address):
    """The measured ledger row for one function, or None if the ledger has no such row."""
    ledger = root / 'ledger/functions.jsonl'
    if not ledger.is_file():
        return None
    wanted = f'{address:#x}'
    with ledger.open(encoding='utf-8') as stream:
        for line in stream:
            if wanted not in line:
                continue
            row = json.loads(line)
            if row.get('module') == module and int(str(row.get('address')), 16) == address:
                return row
    return None


def flag_profile(root, name):
    config = json.loads((root / 'config/source_units.json').read_text(encoding='utf-8-sig'))
    profiles = config.get('flagProfiles') or {}
    if name not in profiles:
        raise SystemExit(f'unknown flag profile {name!r}; known: ' + ', '.join(sorted(profiles)))
    return list(profiles[name])


def default_profile(processor):
    return 'p000' if processor == 'arm7' else 'p001'


def resolved_rule(root, source_path):
    """The source-unit rule the repository build would compile this file under."""
    try:
        relative = source_path.relative_to(root).as_posix()
    except ValueError:
        raise SystemExit(f'--rule needs a source inside the repository: {source_path}')
    if not (root / 'public_tools/source_units.py').is_file():
        raise SystemExit(f'--rule needs a repository checkout with public_tools/: {root}')
    sys.path.insert(0, str(root / 'public_tools'))
    import source_units  # noqa: E402  (public tool, imported lazily)
    config = source_units.load_config(root)
    return source_units.resolve(config, relative)


def detect_function_name(source):
    """The last function definition in the file -- the permuter's ``func_name``."""
    names = [match.group('name') for match in FUNCTION.finditer(source)]
    if not names:
        raise SystemExit('cannot find a function definition in the source; pass --symbol')
    return names[-1]


# ---------------------------------------------------------------- compilers

def compiler_path(root, override=None):
    path = Path(override) if override else root / DEFAULT_COMPILER
    if not path.is_absolute():
        path = root / path
    if not path.is_file():
        raise SystemExit(f'mwccarm is not installed at {path} (tools/ is not committed)')
    return path


def compile_object(root, source, obj, flags, thumb, compiler=None):
    """Compile one translation unit the way the ledger rows were measured."""
    env = dict(os.environ, LM_LICENSE_FILE=str(root / LICENSE))
    command = [str(compiler_path(root, compiler))]
    # -thumb has to precede -c: mwcc reads the mode flag before the compile action.
    command += list(flags) + (['-thumb'] if thumb else []) + ['-c', str(source), '-o', str(obj)]
    return subprocess.run(command, capture_output=True, text=True, env=env)


def object_text(path):
    """(.text bytes, file offset of .text) for an mwccarm object."""
    with open(path, 'rb') as stream:
        elf = ELFFile(stream)
        section = elf.get_section_by_name('.text')
        if section is None:
            raise SystemExit(f'{path}: no .text section')
        return section.data(), section['sh_offset']


def relocation_slots(path):
    """[(offset, kind, symbol)] for the .text relocations, in offset order."""
    with open(path, 'rb') as stream:
        elf = ELFFile(stream)
        symtab = elf.get_section_by_name('.symtab')
        if symtab is None:
            raise SystemExit(f'{path}: no .symtab; cannot read relocation targets')
        slots = []
        for section in elf.iter_sections():
            if section.name not in ('.rel.text', '.rela.text'):
                continue
            for relocation in section.iter_relocations():
                symbol = symtab.get_symbol(relocation['r_info_sym']).name
                slots.append((relocation['r_offset'], relocation['r_info_type'], symbol))
        return sorted(slots)


def build_target_object(base_obj, image_slice, out_path):
    """Rewrite base.o's .text with the measured bytes, zeroing every relocation slot.

    The relocation table is kept: it is what makes the compiled candidate and the
    target diff on equal footing (same symbol names at the same offsets). Slots are
    zeroed because mwccarm leaves an unresolved slot at its addend (0 for a data
    pointer), so a zero there is what a fresh candidate will contain too.
    """
    text, offset = object_text(base_obj)
    if len(text) != len(image_slice):
        raise SystemExit(
            f'refusing: base.c compiles to {len(text)} bytes but the row is '
            f'{len(image_slice)} bytes. The permuter needs a same-size base source; '
            'get the size right (ops/form_search.py) before permuting.')
    target = bytearray(image_slice)
    slots = [slot for slot in relocation_slots(base_obj) if slot[0] + 4 <= len(target)]
    for slot_offset, _, _ in slots:
        target[slot_offset:slot_offset + 4] = b'\0\0\0\0'
    data = bytearray(Path(base_obj).read_bytes())
    data[offset:offset + len(target)] = target
    Path(out_path).write_bytes(bytes(data))
    return {'bytes': len(target), 'slots': [list(slot) for slot in slots],
            'textSha256': sha256(bytes(target)), 'objectSha256': digest_file(out_path)}


# ---------------------------------------------------------------- workspace files

def compile_script(compiler, flags, thumb, license_path):
    rendered = ' '.join(f'"{flag}"' if ' ' in flag else flag for flag in flags)
    thumb_flag = ' -thumb' if thumb else ''
    return (
        '#!/usr/bin/env bash\n'
        '# generated by ops/permuter.py -- decomp-permuter calls: bash compile.sh in.c -o out.o\n'
        'set -euo pipefail\n'
        f'export LM_LICENSE_FILE="{license_path}"\n'
        f'exec "{compiler}" {rendered}{thumb_flag} -c "$1" -o "$3"\n')


def settings_file(symbol, objdump_command, weights):
    lines = [
        '# generated by ops/permuter.py',
        f'func_name = "{symbol}"',
        'compiler_type = "mwcc"',
        # A TOML literal string: the command holds Windows paths, and the permuter
        # runs it through shlex, which would eat backslashes in a basic string.
        f"objdump_command = '{objdump_command}'",
        '',
        '[weight_overrides]',
    ]
    lines += [f'{name} = {value:g}' for name, value in sorted(weights.items())]
    return '\n'.join(lines) + '\n'


def toml_path(path):
    """A shlex/TOML-safe absolute path (shlex would eat Windows backslashes)."""
    return Path(path).as_posix()


def copy_include_closure(source_path, workspace):
    """Copy every quoted include reachable from the source into the workspace.

    Returns ``{basename: origin}``. A header is written under its basename so that a bare
    ``#include "context.h"`` resolves from base.c's directory -- the permuter hardcodes
    ``cpp -P -nostdinc`` with no include path, and its candidate sources are temp files
    elsewhere, so the workdir has to be self-contained.
    """
    copied = {}
    queue = [(source_path, name) for name in QUOTED_INCLUDE.findall(
        source_path.read_text(encoding='utf-8-sig', errors='replace'))]
    while queue:
        origin, name = queue.pop(0)
        if Path(name).is_absolute():
            continue
        candidate = origin.parent / name
        if not candidate.is_file():
            continue
        destination = workspace / Path(name).name
        text = candidate.read_text(encoding='utf-8-sig', errors='replace')
        existing = destination.read_text(encoding='utf-8', errors='replace') if destination.exists() else None
        if existing != text:
            destination.write_text(text, encoding='utf-8', newline='\n')
        copied[Path(name).name] = str(candidate)
        queue.extend((candidate, nested) for nested in QUOTED_INCLUDE.findall(text))
    return copied


def write_workspace(args):
    root = Path(args.root).resolve()
    image, base, image_path = module_info(root, args.module)
    row = ledger_row(root, args.module, int(args.address, 0)) or {}
    address = int(args.address, 0)
    size = args.bytes or row.get('bytes')
    if not size:
        raise SystemExit('no --bytes and the ledger has no row for this address')
    mode = args.mode or row.get('mode') or 'thumb'
    processor = row.get('processor') or ('arm7' if args.module.startswith('arm7') else 'arm9')

    source_path = Path(args.src)
    if not source_path.is_absolute():
        source_path = root / source_path
    if not source_path.is_file():
        raise SystemExit(f'source is missing: {source_path}')
    source_text = source_path.read_text(encoding='utf-8-sig')
    symbol = args.symbol or detect_function_name(source_text)

    if args.rule:
        # The build config is authoritative for a tree source: its rule decides the
        # compiler identity, the flag profile and the mode the project compiles with.
        # Getting this wrong is not cosmetic -- p001 vs p004 changes this row's code.
        unit = resolved_rule(root, source_path)
        mode = unit['mode'] if unit.get('mode') in ('thumb', 'arm') else mode
        flags = [flag for flag in unit['compilerFlags'] if flag != '-thumb']
        args.compiler = unit['compilerPath']
    elif args.flags:
        flags = args.flags.split()
    elif row.get('compilerFlags'):
        flags = row['compilerFlags'].split() if isinstance(row['compilerFlags'], str) else list(row['compilerFlags'])
    else:
        flags = flag_profile(root, args.profile or default_profile(processor))

    # -thumb belongs before -c, added once by compile_object/compile_script; some flag
    # profiles already carry it, so strip it here and let the mode decide.
    thumb = mode == 'thumb' or '-thumb' in flags
    flags = [flag for flag in flags if flag != '-thumb']
    workspace = Path(args.workspace) if args.workspace else WORKSPACES / f'{args.module}_{address:08x}'
    workspace = workspace.resolve()
    if workspace.exists() and any(workspace.iterdir()) and not args.force:
        raise SystemExit(f'{workspace} already has a workspace; pass --force to rebuild')
    workspace.mkdir(parents=True, exist_ok=True)

    scratch = workspace / '.build'
    scratch.mkdir(exist_ok=True)
    base_c = workspace / 'base.c'
    base_c.write_text(source_text, encoding='utf-8')
    # A workdir must preprocess and compile on its own: decomp-permuter hardcodes
    # `cpp -P -nostdinc base.c` with no include path, so quoted headers have to sit next
    # to base.c. Copy the quoted-include closure in (flat, which is how these units spell
    # their includes), and keep going through the copied headers for nested includes.
    headers = copy_include_closure(source_path, workspace)
    base_obj = scratch / 'base.o'
    compiled = compile_object(root, base_c, base_obj, flags, thumb, args.compiler)
    if compiled.returncode != 0:
        raise SystemExit('the base source does not compile:\n'
                         + (compiled.stderr or compiled.stdout).strip()[:1200])

    offset = address - base
    if offset < 0 or offset + size > len(image):
        raise SystemExit(f'{args.module} has no bytes at {address:#x}+{size}')
    image_slice = image[offset:offset + size]
    target = build_target_object(base_obj, image_slice, workspace / 'target.o')

    # The interpreter must be absolute: a bare "python" resolves to the WindowsApps
    # alias stub on some machines and CreateProcess fails with WinError 193.
    objdump_command = (f'{toml_path(sys.executable)} '
                       f'{toml_path(root / "ops/mwcc_objdump.py")} --mode {mode}')
    weights = dict(REGALLOC_WEIGHTS)
    for override in args.weight or []:
        name, _, value = override.partition('=')
        weights[name.strip()] = float(value)
    (workspace / 'compile.sh').write_text(
        compile_script(toml_path(compiler_path(root, args.compiler)),
                       flags, thumb, toml_path(root / LICENSE)),
        encoding='utf-8', newline='\n')
    (workspace / 'settings.toml').write_text(
        settings_file(symbol, objdump_command, weights), encoding='utf-8', newline='\n')

    metadata = {
        'module': args.module,
        'processor': processor,
        'address': f'{address:#010x}',
        'bytes': size,
        'mode': mode,
        'symbol': symbol,
        'ledgerSymbol': row.get('symbol'),
        'ledgerStates': row.get('states'),
        'source': str(source_path.relative_to(root)) if source_path.is_relative_to(root) else str(source_path),
        'sourceSha256': sha256(source_text.encode('utf-8')),
        'compiler': toml_path(compiler_path(root, args.compiler)),
        'flags': flags,
        'thumb': thumb,
        'resolvedFromRule': bool(args.rule),
        'image': str(image_path.relative_to(root)),
        'imageSha256': sha256(image),
        'imageSliceSha256': sha256(image_slice),
        'target': target,
        'permuterPin': PERMUTER_PIN,
        'objdumpCommand': objdump_command,
        'headers': headers,
        'weights': weights,
        'createdAt': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
    }
    (workspace / 'row.json').write_text(json.dumps(metadata, indent=2) + '\n',
                                        encoding='utf-8')
    (workspace / 'README.md').write_text(
        f'# {args.module} {address:#010x} ({size} B, {mode})\n\n'
        f'Generated by `ops/permuter.py`. Source: `{metadata["source"]}`. '
        f'Symbol: `{symbol}`.\n\n'
        f'    python ops/permuter.py probe .        # base score through the real shim\n'
        f'    python ops/permuter.py run . --timeout 300\n'
        f'    python ops/verify_permuter.py . --source best.c\n',
        encoding='utf-8')

    print(f'workspace  {workspace}')
    print(f'row        {args.module} {address:#010x}  {size} B  {mode}  {symbol}')
    print(f'flags      {" ".join(flags)}' + (' -thumb' if thumb else ''))
    targets = ', '.join(sorted({slot[2] for slot in target['slots']})) or '(none)'
    print(f'target.o   {size} B of image bytes, '
          f'{len(target["slots"])} relocation slot(s) zeroed: '
          + ', '.join(f'{slot[0]:#x}' for slot in target['slots']))
    print(f'           relocation targets: {targets}')
    print(f'objdump    {objdump_command}')
    print('next       python ops/permuter.py probe ' + str(workspace))
    return 0


# ---------------------------------------------------------------- running

def find_permuter(root, explicit=None):
    """Locate the pinned decomp-permuter checkout and prove the revision."""
    candidates = [explicit, os.environ.get('DECOMP_PERMUTER'),
                  root / 'work/decomp-permuter',
                  root / f'tools/decomp-permuter-{PERMUTER_PIN}']
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate)
        if not path.is_absolute():
            path = root / path
        if not (path / 'permuter.py').is_file():
            continue
        git = path / '.git'
        if git.exists():
            head = subprocess.run(['git', '-C', str(path), 'rev-parse', 'HEAD'],
                                  capture_output=True, text=True)
            if head.returncode != 0 or head.stdout.strip() != PERMUTER_PIN:
                raise SystemExit(
                    f'{path} is not at the pinned commit {PERMUTER_PIN} '
                    f'(found {head.stdout.strip()[:12] or "unknown"}); '
                    f're-clone: git clone {PERMUTER_REPOSITORY} && git checkout {PERMUTER_PIN}')
        return path
    raise SystemExit(
        'decomp-permuter is not installed. Clone it OUTSIDE git (work/ is ignored):\n'
        f'  git clone {PERMUTER_REPOSITORY} work/decomp-permuter\n'
        f'  git -C work/decomp-permuter checkout {PERMUTER_PIN}\n'
        f'or run python {PERMUTER_ACQUIRE} (imports the same commit under tools/).')


def bash_for_permuter():
    """decomp-permuter requires `bash`; put a POSIX one ahead of the WSL launcher."""
    which = shutil.which('bash')
    if which and 'system32' not in which.lower():
        return which
    for candidate in (r'C:\Program Files\Git\bin\bash.exe',
                      r'C:\Program Files\Git\usr\bin\bash.exe'):
        if Path(candidate).is_file():
            return candidate
    if which:
        return which
    raise SystemExit('no bash on PATH; decomp-permuter needs one (Git for Windows provides it)')


def link_or_copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        return destination
    try:
        os.link(source, destination)
    except OSError:
        shutil.copyfile(source, destination)
    return destination


def ensure_cpp(root):
    """decomp-permuter hardcodes ``cpp``; provide the NDK's clang under that name.

    ``src/preprocess.py`` shells out to ``cpp -P -nostdinc -DPERMUTER base.c`` with no
    way to configure it, and this machine (like most Windows boxes) has no GCC-style
    ``cpp``. LLVM's driver does behave as a preprocessor when its program name is
    ``cpp``, so a hardlink next to the pinned NDK clang is enough -- but it has to keep
    that clang's directory for its DLLs, hence a small private bin directory that is
    prepended to PATH only for the permuter process.
    """
    which = shutil.which('cpp')
    if which and 'windowsapps' not in which.lower():
        return which
    clang = next(iter(sorted(root.glob(
        'tools/android-ndk/*/toolchains/llvm/prebuilt/windows-*/bin/clang.exe'))), None)
    if clang is None:
        raise SystemExit('no `cpp` on PATH and no pinned NDK clang to stand in for it; '
                         'install a C preprocessor or the android-ndk toolchain')
    bindir = root / 'work/permuter/.bin'
    cpp = link_or_copy(clang, bindir / 'cpp.exe')
    for library in clang.parent.glob('*.dll'):
        link_or_copy(library, bindir / library.name)
    return cpp


def permuter_environment(root):
    """Environment for a permuter child: POSIX bash, a `cpp`, and no Windows aliases."""
    environment = dict(os.environ)
    bash = bash_for_permuter()
    cpp = ensure_cpp(root)
    environment['PATH'] = os.pathsep.join(
        [str(Path(cpp).parent), str(Path(bash).parent), environment.get('PATH', '')])
    environment['PYTHONIOENCODING'] = 'utf-8'
    return environment


ANSI = re.compile(r'[\b\r]|\x1b\[[0-9;]*[A-Za-z]')


def run_permuter(root, workspace, timeout, extra, permuter, threads=None):
    workspace = Path(workspace).resolve()
    metadata = json.loads((workspace / 'row.json').read_text(encoding='utf-8'))
    environment = permuter_environment(root)
    command = [sys.executable, str(permuter / 'permuter.py'), '.', '--stop-on-zero']
    if threads:
        command += ['-j', str(threads)]
    command += list(extra or [])
    log_path = workspace / 'run.log'
    started = time.time()
    with log_path.open('w', encoding='utf-8', errors='replace') as log:
        process = subprocess.Popen(command, cwd=str(workspace), stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                                   errors='replace', env=environment)
        timed_out = False
        try:
            output, _ = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            process.kill()
            output, _ = process.communicate()
        log.write(output or '')
    elapsed = round(time.time() - started, 1)
    clean = ANSI.sub('', output or '')

    base_score = re.search(r'base score = (-?\d+)', clean)
    iterations = [int(value) for value in re.findall(r'iteration (\d+),', clean)]
    outputs = [(int(score), int(counter), workspace / f'output-{score}-{counter}')
               for score, counter in re.findall(r'wrote to .*?output-(-?\d+)-(\d+)', clean)]
    outputs.sort()
    result = {
        'workspace': str(workspace),
        'module': metadata['module'],
        'address': metadata['address'],
        'bytes': metadata['bytes'],
        'symbol': metadata['symbol'],
        'compiler': metadata['compiler'],
        'permuter': str(permuter),
        'permuterPin': PERMUTER_PIN,
        'command': command,
        'timeoutSeconds': timeout,
        'timedOut': timed_out,
        'returncode': process.returncode,
        'elapsedSeconds': elapsed,
        'baseScore': int(base_score.group(1)) if base_score else None,
        'iterations': max(iterations) if iterations else None,
        'outputs': [{'score': score, 'directory': directory.name} for score, _, directory in outputs],
        'bestScore': outputs[0][0] if outputs else None,
        'exact': bool(outputs) and outputs[0][0] == 0,
        'log': log_path.name,
    }
    if outputs:
        best = outputs[0][2]
        shutil.copyfile(best / 'source.c', workspace / 'best.c')
        diff = (best / 'diff.txt')
        if diff.is_file():
            (workspace / 'best.diff').write_text(diff.read_text(encoding='utf-8'), encoding='utf-8')
        result['best'] = best.name
    (workspace / 'run.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')

    print(f'{"stopped on timeout" if timed_out else "permuter exited"} after {elapsed}s '
          f'({result["outputs"].__len__()} scored output(s), base score {result["baseScore"]})')
    if not outputs:
        print('no output directories: every candidate failed to compile or to score.')
        print('first log lines:')
        for line in [row for row in clean.splitlines() if row.strip()][:12]:
            print('  ' + line)
        return 1
    print(f'best score {result["bestScore"]} in {result["best"]}'
          + ('  <-- EXACT, now run ops/verify_permuter.py' if result['exact'] else ''))
    if result.get('best'):
        print(f'winning source copied to {workspace / "best.c"}')
    return 0


def probe_workspace(root, workspace, permuter):
    """Run decomp-permuter's own setup+score path once (``--debug``) to prove it parses."""
    workspace = Path(workspace).resolve()
    environment = permuter_environment(root)
    command = [sys.executable, str(permuter / 'permuter.py'), '.', '--debug']
    completed = subprocess.run(command, cwd=str(workspace), capture_output=True, text=True,
                               encoding='utf-8', errors='replace', env=environment)
    clean = ANSI.sub('', (completed.stdout or '') + (completed.stderr or ''))
    score = re.search(r'base score = (-?\d+)', clean)
    if completed.returncode != 0 or not score:
        print('the permuter could not set up this workspace:')
        for line in [row for row in clean.splitlines() if row.strip()][:20]:
            print('  ' + line)
        return 1
    print(f'permuter accepted the workspace: base score {score.group(1)} '
          f'(0 would mean the row is already exact)')
    metadata_path = workspace / 'row.json'
    if metadata_path.is_file():
        metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
        metadata['baseScore'] = int(score.group(1))
        metadata['probedAt'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
        metadata_path.write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    return 0


# ---------------------------------------------------------------- CLI

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='command', required=True)

    build = sub.add_parser('build', help='generate the permuter workspace for one row')
    build.add_argument('--module', required=True)
    build.add_argument('--address', required=True)
    build.add_argument('--src', required=True, help='current best-known source for the row')
    build.add_argument('--symbol', help='C function name (default: detected from --src)')
    build.add_argument('--bytes', type=lambda value: int(value, 0))
    build.add_argument('--mode', choices=('thumb', 'arm'))
    build.add_argument('--flags', help='exact compiler flags (default: ledger or flag profile)')
    build.add_argument('--rule', action='store_true',
                       help='take compiler, flags and mode from config/source_units.json for --src')
    build.add_argument('--profile', help='flag profile from config/source_units.json')
    build.add_argument('--compiler', help='mwccarm build (default: 2.0/base)')
    build.add_argument('--weight', action='append', metavar='NAME=VALUE',
                       help='override one randomization weight (repeatable)')
    build.add_argument('--workspace', help='workspace directory (default: work/permuter/<module>_<addr>)')
    build.add_argument('--root', default=str(ROOT))
    build.add_argument('--force', action='store_true')
    build.set_defaults(func=write_workspace)

    run = sub.add_parser('run', help='run decomp-permuter over a workspace for a bounded time')
    run.add_argument('workspace')
    run.add_argument('--timeout', type=float, default=300.0, help='wall-clock seconds (default 300)')
    run.add_argument('--threads', type=int, help='permuter -j (multiprocessing is broken on Windows; leave unset)')
    run.add_argument('--permuter', help='decomp-permuter checkout')
    run.add_argument('--extra', action='append', help='extra permuter flag (repeatable)')
    run.add_argument('--root', default=str(ROOT))
    run.set_defaults(func=lambda args: run_permuter(
        Path(args.root).resolve(), args.workspace, args.timeout, args.extra,
        find_permuter(Path(args.root).resolve(), args.permuter), args.threads))

    probe = sub.add_parser('probe', help="parse-check a workspace with the permuter's own scorer")
    probe.add_argument('workspace')
    probe.add_argument('--permuter', help='decomp-permuter checkout')
    probe.add_argument('--root', default=str(ROOT))
    probe.set_defaults(func=lambda args: probe_workspace(
        Path(args.root).resolve(), args.workspace,
        find_permuter(Path(args.root).resolve(), args.permuter)))

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
