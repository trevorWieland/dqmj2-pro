"""Repository-driven compilation and objdiff measurement.

The unit of work is a source file, not a function listed in an evidence
manifest.  Every ``src/**/*.c`` (excluding ``src/nonmatching/**``) is resolved
to a rule in ``config/source_units.json``, compiled with that rule's flags, and
then measured against the original module image at the ledger address encoded
in its symbol name.

``complete`` is computed from the bytes: the compiled function is patched with
its ELF relocations using the measured original symbol addresses and compared
with the original image.  A unit is complete only when every byte agrees.
"""

import argparse
import collections
import concurrent.futures
import contextlib
import hashlib
import json
import os
import re
import struct
import subprocess
import tempfile
import time
from pathlib import Path, PurePosixPath

from bytematch_project import DENOMINATOR, elf_object, write
from source_units import CONFIG, SourceUnitError, enumerate_sources, load_config, read_json

MODNAMES = ('main', 'itcm', 'dtcm', 'ov000', 'ov001', 'ov002', 'ov003', 'ov004', 'ov005', 'ov006', 'ov007',
            'arm7-boot', 'arm7-wram', 'arm7-main', 'utility-child-arm9-main', 'utility-child-arm9-itcm',
            'utility-child-arm9-dtcm', 'utility-child-arm7-boot', 'utility-child-arm7-wram',
            'utility-child-arm7-main')
CATEGORIES = [{'id': name, 'name': label} for name, label in (
    ('host_arm9', 'Host ARM9'), ('host_arm7', 'Host ARM7'),
    ('child_arm9', 'Embedded child ARM9'), ('child_arm7', 'Embedded child ARM7'),
    ('unclassified', 'Unclassified initialized-byte budget (no function claim)'))]
DATA_KINDS = {'data', 'rodata', 'initialized-data'}
ADDRESS = re.compile(r'([0-9a-fA-F]{8})$')
COMPILE_SUFFIXES = ('.c',)


class RepositoryBuildError(ValueError):
    pass


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def module_inventory(root, config):
    table = config['modules']
    if len(table) != 20:
        raise RepositoryBuildError('The source-unit configuration must describe all twenty modules')
    if set(table) != set(MODNAMES):
        raise RepositoryBuildError('Source-unit module inventory differs from the measured module set')
    if sum(int(entry['bytes']) for entry in table.values()) != DENOMINATOR:
        raise RepositoryBuildError('Source-unit module inventory does not cover the initialized denominator')
    return table


def image_path(root, module):
    return (Path(root) / module['originalImage'].replace('\\', '/')).resolve()


def compiler_inventory(root, config):
    inventory = config['compilers']
    resolved = {}
    for identity, relative in inventory.items():
        path = Path(root) / relative
        if not path.is_file():
            raise RepositoryBuildError('Pinned compiler is unavailable: ' + relative)
        if digest(path) != identity:
            raise RepositoryBuildError('Pinned compiler identity differs: ' + relative)
        resolved[identity] = path
    default = config['default_compiler']
    if default not in resolved:
        raise RepositoryBuildError('The default compiler identity is absent from the inventory')
    license_file = None
    for candidate in (resolved[default].parent.parent.parent / 'license.dat',
                      resolved[default].parent.parent / 'license.dat',
                      resolved[default].parent / 'license.dat'):
        if candidate.is_file():
            license_file = candidate
            break
    return resolved, license_file, default


@contextlib.contextmanager
def short_paths(root):
    """Give the 32-bit compiler a drive-substituted view of very long paths."""
    root = Path(root).resolve()

    def identity(path):
        return str(Path(path).resolve())

    drive = None
    if os.name == 'nt':
        used = {path.drive.upper() for path in [Path.cwd(), root] if path.drive}
        for letter in 'QRSTUVWXYZ':
            candidate = letter + ':'
            if candidate in used:
                continue
            result = subprocess.run(['subst', candidate, str(root)], capture_output=True, text=True)
            if result.returncode == 0:
                drive = candidate
                break
    try:
        if drive is None:
            yield root, identity
        else:
            def short(path):
                path = Path(path).resolve()
                if not path.is_relative_to(root):
                    return str(path)
                return drive + '\\' + str(path.relative_to(root)).replace('/', '\\')
            yield root, short
    finally:
        if drive is not None:
            subprocess.run(['subst', drive, '/D'], capture_output=True, text=True)


def compile_all(root, private_root, out_dir, jobs=4, timeout=180, limit=None, sources=None):
    root, private = Path(root).resolve(), Path(private_root).resolve()
    config = load_config(root)
    inventory = module_inventory(root, config)
    compilers, license_file, default_compiler = compiler_inventory(root, config)
    enumerated = enumerate_sources(root, config)
    selected = [unit for unit in enumerated['compiled'] if unit['path'].endswith(COMPILE_SUFFIXES)]
    if sources:
        wanted = {name.replace('\\', '/') for name in sources}
        selected = [unit for unit in selected if unit['path'] in wanted]
        missing = wanted - {unit['path'] for unit in selected}
        if missing:
            raise RepositoryBuildError('Requested source is not a compiled repository unit: ' + ', '.join(sorted(missing)[:5]))
    if limit:
        selected = selected[:limit]
    out_dir = Path(out_dir).resolve()
    if not out_dir.is_relative_to(root / 'build') and not out_dir.is_relative_to(root / 'work'):
        raise RepositoryBuildError('Compilation output must remain beneath build/ or work/')
    objects = out_dir / 'objects'
    objects.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    if license_file is not None:
        env['LM_LICENSE_FILE'] = str(license_file)
    started = time.time_ns()

    def compile_unit(task, short):
        source = (root / task['path']).resolve()
        if not source.is_file():
            raise RepositoryBuildError('Source file disappeared: ' + task['path'])
        identity = json.dumps([task['path'], task['compilerSha256'], task['profileFlags'],
                               task.get('alternateIndex')], sort_keys=True)
        key = hashlib.sha256(identity.encode()).hexdigest()[:24]
        obj = objects / (key + '.o')
        flags = list(task['profileFlags'])
        if '-c' not in flags:
            flags.append('-c')
        compiler = compilers[task['compilerSha256']]
        record = dict(source=task['path'], module=task['module'], processor=task['processor'],
                      compilerFlags=flags, object=obj.relative_to(root).as_posix(),
                      compilerSha256=task['compilerSha256'], alternate=task.get('alternate', False),
                      alternateIndex=task.get('alternateIndex'), startedTimeNs=time.time_ns())
        try:
            argv = [str(compiler), *flags, Path(short(source)).name, '-o', short(obj)]
            process = subprocess.run(argv, cwd=short(source.parent), env=env,
                                     capture_output=True, timeout=timeout)
            record.update(exitCode=process.returncode,
                          stdoutTail=process.stdout.decode(errors='replace')[-400:],
                          stderrTail=process.stderr.decode(errors='replace')[-400:])
            if process.returncode or not obj.is_file():
                record.update(status='compile-failed', objectSha256=None)
                return record
            record.update(status='compiled', objectSha256=digest(obj))
        except (OSError, subprocess.TimeoutExpired, RepositoryBuildError) as error:
            record.update(status='compile-or-object-failed', exitCode=-1, error=type(error).__name__ + ': ' + str(error))
        return record

    tasks = []
    for unit in selected:
        tasks.append(dict(unit, profileFlags=unit['compilerFlags'], alternate=False))
        for index, alternate in enumerate(unit.get('alternates', [])):
            tasks.append(dict(unit, profileFlags=alternate['compilerFlags'], alternate=True,
                              alternateIndex=index, compilerSha256=alternate['compilerSha256']))
    with short_paths(root) as (unused_root, short):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, min(int(jobs), 16))) as pool:
            results = list(pool.map(lambda task: compile_unit(task, short), tasks))
    if any(digest(path) != identity for identity, path in compilers.items()):
        raise RepositoryBuildError('A pinned compiler changed during repository compilation')
    compiled = [record for record in results if record.get('status') == 'compiled']
    failed = [record for record in results if record.get('status') != 'compiled']
    primary = [record for record in results if not record.get('alternate')]
    primary_compiled = [record for record in primary if record.get('status') == 'compiled']
    primary_failed = [record for record in primary if record.get('status') != 'compiled']
    report = dict(
        schemaVersion=2,
        status='source-compilation-passed' if not failed else 'source-compilation-partial',
        startedTimeNs=started, finishedTimeNs=time.time_ns(),
        compiler=dict(path=config['data']['compiler']['path'], sha256=default_compiler),
        compilers={identity: path.relative_to(root).as_posix() for identity, path in sorted(compilers.items())},
        configSha256=digest(root / CONFIG),
        sourceInventory=dict(allSourceFiles=len(enumerated['files']),
                             compiledSources=len(enumerated['compiled']),
                             excludedSources=len(enumerated['excluded'])),
        selectedCompilationUnits=len(selected), compiledUnits=len(primary_compiled),
        failedUnits=len(primary_failed), alternateCompilations=len(tasks) - len(selected),
        fullRepositoryCompiled=len(primary) == len(selected) == len(enumerated['compiled']),
        compilePolicy='Every resolved C source is compiled. A non-ledger draft that does not compile is recorded '
                      'as an unmeasured unit; it never becomes source credit. An unresolved rule is fatal.',
        results=[dict(record) for record in compiled],
        failures=[{key: record.get(key) for key in ('source', 'module', 'status', 'exitCode', 'stderrTail', 'error',
                                                    'alternate', 'alternateIndex')}
                  for record in failed],
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    write(out_dir / 'report.json', report)
    return report


# ---------------------------------------------------------------------------
# ELF inspection


def elf_sections(raw):
    if raw[:7] != b'\x7fELF\x01\x01\x01' or len(raw) < 52:
        raise RepositoryBuildError('Compiled source is not an ARM ELF32 object')
    header = struct.unpack_from('<16sHHIIIIIHHHHHH', raw)
    if header[1:4] != (1, 40, 1) or header[11] != 40:
        raise RepositoryBuildError('Compiled source is not a relocatable ARM ELF32 object')
    if header[6] + header[12] * 40 > len(raw):
        raise RepositoryBuildError('ELF section table escapes its object')
    sections = [struct.unpack_from('<IIIIIIIIII', raw, header[6] + 40 * index)
                for index in range(header[12])]
    return header, sections


def section_body(raw, section):
    if section[4] + section[5] > len(raw):
        raise RepositoryBuildError('ELF section payload escapes its object')
    return raw[section[4]:section[4] + section[5]]


def elf_symbols(raw, sections):
    tables = {}
    for index, section in enumerate(sections):
        if section[1] != 2 or section[6] >= len(sections):
            continue
        strings = section_body(raw, sections[section[6]])
        table = []
        for offset in range(0, section[5], 16):
            name_at, value, size, info, other, shndx = struct.unpack_from('<IIIBBH', section_body(raw, section), offset)
            end = strings.find(b'\0', name_at)
            if end < 0:
                raise RepositoryBuildError('Invalid ELF symbol name')
            table.append(dict(name=strings[name_at:end].decode('utf-8', 'replace'), value=value, size=size,
                              info=info, other=other, shndx=shndx))
        tables[index] = table
    return tables


def elf_profile(raw):
    header, sections = elf_sections(raw)
    names = section_body(raw, sections[header[13]])
    def name(index):
        end = names.find(b'\0', sections[index][0])
        return names[sections[index][0]:end].decode('utf-8', 'replace')
    symbols = elf_symbols(raw, sections)
    functions = []
    for index, section in enumerate(sections):
        if section[1] != 2:
            continue
        for symbol in symbols[index]:
            if symbol['info'] & 0xF != 2 or not symbol['size'] or not symbol['shndx'] < len(sections):
                continue
            target = sections[symbol['shndx']]
            if not target[2] & 4:
                continue
            start = symbol['value'] & ~1
            if start + symbol['size'] > target[5]:
                raise RepositoryBuildError('ELF function escapes its section')
            functions.append(dict(name=symbol['name'], value=start, size=symbol['size'],
                                  section=symbol['shndx'],
                                  mode='thumb' if symbol['value'] & 1 else 'arm',
                                  bytes=bytearray(section_body(raw, target)[start:start + symbol['size']])))
    relocations = collections.defaultdict(list)
    for index, section in enumerate(sections):
        if section[1] not in (4, 9) or section[7] >= len(sections) or section[6] not in symbols:
            continue
        table = symbols[section[6]]
        step = 12 if section[1] == 4 else 8
        for offset in range(0, section[5], step):
            where, info = struct.unpack_from('<II', section_body(raw, section), offset)
            symbol = table[info >> 8]
            addend = struct.unpack_from('<i', section_body(raw, section), offset + 8)[0] if step == 12 else None
            relocations[section[7]].append(dict(where=where, type=info & 255, symbol=symbol, addend=addend))
    sections = [dict(index=index, name=name(index), type=section[1], flags=section[2], address=section[3],
                     offset=section[4], size=section[5], link=section[6], info=section[7], align=section[8])
                for index, section in enumerate(sections)]
    return dict(functions=functions, relocations=relocations, sections=sections)


def sign_extend(value, bits):
    if value & (1 << (bits - 1)):
        value -= 1 << bits
    return value


def decode_original_target(kind, image, absolute, base):
    offset = absolute - base
    if offset < 0 or offset + 4 > len(image):
        return None
    if kind == 1:
        word = struct.unpack_from('<I', image, offset)[0]
        return (absolute + 8 + (sign_extend(word & 0xFFFFFF, 24) << 2)) & ~0, 'arm'
    if kind == 2:
        value = struct.unpack_from('<I', image, offset)[0]
        return value, ('thumb' if value & 1 else 'arm')
    if kind == 10:
        high, low = struct.unpack_from('<HH', image, offset)
        s = (high >> 10) & 1
        j1, j2 = (low >> 13) & 1, (low >> 11) & 1
        i1, i2 = 1 - (j1 ^ s), 1 - (j2 ^ s)
        immediate = (s << 24) | (i1 << 23) | (i2 << 22) | ((high & 0x3FF) << 12) | ((low & 0x7FF) << 1)
        immediate = sign_extend(immediate, 25)
        if (low & 0xF800) == 0xE800:
            return ((absolute + 4) & ~3) + immediate, 'arm'
        return absolute + 4 + immediate, 'thumb'
    return None


def symbol_address(symbol, module, base, function, sections):
    name = symbol['name']
    runtime = module.get('runtime', {})
    if name:
        if (module.get('name'), name) in runtime:
            return runtime[(module['name'], name)][0]
        if ('*', name) in runtime:
            return runtime[('*', name)][0]
        row = module['symbols'].get(name)
        if row is not None:
            return int(row['address'], 0)
        match = ADDRESS.search(name)
        if match:
            return int(match.group(1), 16)
    if symbol['shndx'] < len(sections):
        section = sections[symbol['shndx']]
        if symbol['shndx'] == function['section']:
            return function['address'] - function['value'] + symbol['value']
    return None


def target_mode(module, address, name=None):
    runtime = module.get('runtime', {})
    if name:
        if (module.get('name'), name) in runtime:
            return runtime[(module['name'], name)][1]
        if ('*', name) in runtime:
            return runtime[('*', name)][1]
    row = module.get('by_address', {}).get(address)
    if row is not None:
        return row.get('mode')
    return None


def patch_function(function, module, base, sections, relocations, image):
    body = bytearray(function['bytes'])
    unresolved = []
    for relocation in relocations.get(function['section'], []):
        if not (function['value'] <= relocation['where'] < function['value'] + function['size']):
            continue
        offset = relocation['where'] - function['value']
        target = symbol_address(relocation['symbol'], module, base, function, sections)
        addend = relocation['addend']
        kind = relocation['type']
        absolute = function['address'] + offset
        mode = target_mode(module, target, relocation['symbol']['name']) if target is not None else None
        if kind in (1, 10) and relocation['symbol']['shndx'] == 0:
            decoded = decode_original_target(kind, image, absolute, base)
            if decoded is not None:
                target, mode = decoded
        if kind == 2 and target is None:
            decoded = decode_original_target(kind, image, absolute, base)
            if decoded is not None:
                target, mode = decoded
                addend = 0
        if target is None:
            unresolved.append(relocation['symbol']['name'])
            continue
        if kind == 1:  # R_ARM_PC24
            word = struct.unpack_from('<I', body, offset)[0]
            if addend is None:
                encoded = struct.unpack_from('<i', struct.pack('<I', word << 8))[0] >> 8
                addend = encoded * 4
            immediate = (target + addend - absolute) >> 2
            struct.pack_into('<I', body, offset, (word & 0xFF000000) | (immediate & 0xFFFFFF))
        elif kind == 2:  # R_ARM_ABS32
            if addend is None:
                addend = 0
            value = target + addend
            if mode == 'thumb':
                value |= 1
            struct.pack_into('<I', body, offset, value & 0xFFFFFFFF)
        elif kind in (10, 11):  # R_ARM_THM_CALL / R_ARM_THM_JUMP24
            if addend is None:
                addend = 0
            if kind == 10 and mode == 'arm':
                immediate = (target + addend - (absolute & ~3)) >> 1
                low = 0xE800
            else:
                immediate = (target + addend - absolute) >> 1
                low = 0xF800
            high = 0xF000 if kind == 10 else 0x9000
            struct.pack_into('<H', body, offset, high | ((immediate >> 11) & 0x7FF))
            struct.pack_into('<H', body, offset + 2, low | (immediate & 0x7FF))
        elif kind in (43, 44):  # R_ARM_MOVW_ABS_NC / R_ARM_MOVT_ABS
            if addend is None:
                addend = 0
            value = target + addend
            if kind == 43 and mode == 'thumb':
                value |= 1
            immediate = value & 0xFFFF if kind == 43 else (value >> 16) & 0xFFFF
            word = struct.unpack_from('<I', body, offset)[0]
            word = (word & ~0x000F0FFF) | ((immediate & 0xF000) << 4) | (immediate & 0x0FFF)
            struct.pack_into('<I', body, offset, word)
        else:
            unresolved.append(relocation['symbol']['name'])
    return bytes(body), unresolved


def ledger_index(private_root):
    path = Path(private_root) / 'ledger/functions.jsonl'
    if not path.is_file():
        raise RepositoryBuildError('The private address ledger is unavailable: ' + str(path))
    by_address, by_symbol, by_source = {}, {}, collections.defaultdict(list)
    count = 0
    with path.open(encoding='utf-8') as stream:
        for line in stream:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            size = row.get('bytes')
            if type(size) is not int or size <= 0:
                continue
            address = int(row['address'], 0)
            by_address.setdefault((row['module'], address), row)
            by_symbol.setdefault((row['module'], row['symbol']), row)
            source = (row.get('sourceUnit') or '').replace('\\', '/')
            if source.endswith(('.c', '.s')):
                by_source[(row['module'], source)].append(row)
            count += 1
    for rows in by_source.values():
        rows.sort(key=lambda item: int(item['address'], 0))
    return by_address, by_symbol, by_source, count


def accepted_data(root, build_sha256):
    path = Path(root) / 'public/accepted-data.json'
    if not path.is_file():
        return {}
    document = read_json(path)
    if build_sha256 is not None and document.get('buildSha256') != build_sha256:
        raise RepositoryBuildError('Typed-data snapshot belongs to another measured build')
    spans = collections.defaultdict(list)
    for row in document.get('records', []):
        if row.get('kind') == 'bss':
            continue
        if row.get('kind') not in DATA_KINDS:
            raise RepositoryBuildError('Unsupported typed-data kind: ' + str(row.get('kind')))
        if row.get('states', {}).get('dataMatched') is not True or row.get('states', {}).get('moduleLinked') is not True:
            raise RepositoryBuildError('Typed-data snapshot contains unqualified initialized data')
        size = row.get('bytes')
        if type(size) is not int or size <= 0 or row.get('storedBytes') != size:
            raise RepositoryBuildError('Typed-data extent differs')
        start = int(row['address'], 0)
        spans[row['module']].append(dict(start=start, end=start + size, source=row['source'].replace('\\', '/'),
                                         symbol=row.get('symbol')))
    return spans


def original_sections(root, name, module):
    if module.get('program') or module['processor'] != 'arm9':
        return []
    folder = Path('config/arm9') / ('overlays/' + name if name.startswith('ov') else name if name != 'main' else '')
    path = Path(root) / folder / 'delinks.txt'
    if not path.is_file():
        return []
    result = []
    for line in path.read_text().splitlines():
        match = re.match(r'\s+\.\S+\s+start:(0x[0-9a-fA-F]+) end:(0x[0-9a-fA-F]+) kind:(code|data|rodata)\b', line)
        if match and int(match[2], 0) > int(match[1], 0):
            result.append((int(match[1], 0), int(match[2], 0), match[3] == 'code'))
    return result


# ---------------------------------------------------------------------------
# Measurement


def image_cache(root, modules):
    cache = {}
    for name, module in modules.items():
        path = image_path(root, module)
        if not path.is_file():
            raise RepositoryBuildError('Original module image is unavailable: ' + module['originalImage'])
        image = path.read_bytes()
        if len(image) != module['bytes']:
            raise RepositoryBuildError('Original module image size differs: ' + name)
        cache[name] = image
    return cache


def recover_runtime_symbols(root, report, modules, images, by_address, by_symbol, addresses_by_module):
    """Recover linker-resolved runtime/libc symbol addresses from the original image.

    A few compiler-runtime helpers (``_ffix``, ``_fmul``, ``strlen``, ...) are
    resolved by the original linker from libraries that are not part of the
    public tree.  Their call sites exist in the original image, so the target
    address can be read from the original instruction.  A name is admitted only
    when its decoded address is consistent across at least one site.
    """
    candidates = collections.defaultdict(collections.Counter)
    global_addresses = {}
    for (module_name, address), row in by_address.items():
        global_addresses.setdefault(address, row)
    symbols_by_module = collections.defaultdict(dict)
    for (module_name, symbol), row in by_symbol.items():
        symbols_by_module[module_name][symbol] = row
    for record in report.get('results', []):
        if record.get('status') != 'compiled':
            continue
        profile = elf_profile((Path(root) / record['object']).read_bytes())
        module = dict(modules[record['module']])
        module['name'] = record['module']
        module['symbols'] = symbols_by_module.get(record['module'], {})
        module['by_address'] = addresses_by_module.get(record['module'], {})
        module['global_addresses'] = global_addresses
        base = int(module['loadAddressBase'], 0)
        image = images[record['module']]
        for function in profile['functions']:
            match = ADDRESS.search(function['name'])
            if not match:
                continue
            address = int(match.group(1), 16)
            if (record['module'], address) not in by_address:
                continue
            function['address'] = address
            for relocation in profile['relocations'].get(function['section'], []):
                if not (function['value'] <= relocation['where'] < function['value'] + function['size']):
                    continue
                if relocation['symbol']['shndx'] != 0:
                    continue
                if relocation['symbol']['name'] in module['symbols']:
                    continue
                decoded = decode_original_target(relocation['type'], image,
                                                 address + (relocation['where'] - function['value']), base)
                if decoded is None:
                    continue
                value, mode = decoded
                if mode == 'thumb':
                    value &= ~1
                candidates[(record['module'], relocation['symbol']['name'])][(value, mode)] += 1
    runtime = {}
    for (module_name, name), values in candidates.items():
        (value, mode), count = values.most_common(1)[0]
        runtime[(module_name, name)] = (value, mode)
    return runtime


def compiled_selections(root, private_root, compilation):
    report = read_json(compilation)
    if report.get('schemaVersion') != 2:
        raise RepositoryBuildError('A repository compilation report is required')
    if report.get('selectedCompilationUnits') != (report.get('compiledUnits', 0) + report.get('failedUnits', 0)):
        raise RepositoryBuildError('The compilation report did not account for every selected source')
    if digest(root / CONFIG) != report.get('configSha256'):
        raise RepositoryBuildError('The source-unit configuration changed after compilation')
    config = load_config(root)
    modules = module_inventory(root, config)
    images = image_cache(root, modules)
    by_address, by_symbol, by_source, unused_ledger_rows = ledger_index(private_root)
    symbols_by_module = collections.defaultdict(dict)
    for (module_name, symbol), row in by_symbol.items():
        symbols_by_module[module_name][symbol] = row
    addresses_by_module = collections.defaultdict(dict)
    for (module_name, address), row in by_address.items():
        addresses_by_module[module_name][address] = row
    global_addresses = {}
    for (module_name, address), row in by_address.items():
        global_addresses.setdefault(address, row)
    runtime = recover_runtime_symbols(root, report, modules, images, by_address, by_symbol, addresses_by_module)
    selections = collections.defaultdict(dict)
    stats = dict(compiledObjects=0, mappedFunctions=0, exactFunctions=0, unmatchedFunctions=0,
                 duplicateAddresses=0, unresolvedRelocations=0, runtimeSymbols=len(runtime),
                 compileFailures=len(report.get('failures', [])))
    for record in report.get('results', []):
        if record.get('status') != 'compiled':
            continue
        obj = (root / record['object']).resolve()
        if not obj.is_file() or digest(obj) != record.get('objectSha256'):
            raise RepositoryBuildError('Fresh compiled object missing or changed: ' + str(record.get('source')))
        profile = elf_profile(obj.read_bytes())
        stats['compiledObjects'] += 1
        module = dict(modules[record['module']])
        module['name'] = record['module']
        module['symbols'] = symbols_by_module.get(record['module'], {})
        module['by_address'] = addresses_by_module.get(record['module'], {})
        module['global_addresses'] = global_addresses
        module['runtime'] = runtime
        base = int(module['loadAddressBase'], 0)
        image = images[record['module']]
        source_rows = list(by_source.get((record['module'], record['source'].replace('\\', '/')), []))
        used_addresses = set()
        functions = sorted(profile['functions'], key=lambda item: (item['section'], item['value']))

        def direct_row(function):
            match = ADDRESS.search(function['name'])
            return by_address.get((record['module'], int(match.group(1), 16))) if match else None

        direct_rows = [direct_row(function) for function in functions]
        direct_addresses = {int(row['address'], 0) for row in direct_rows if row is not None}
        remaining_rows = [row for row in source_rows if int(row['address'], 0) not in direct_addresses]
        order_pair = len(functions) - len([row for row in direct_rows if row is not None]) == len(remaining_rows)
        provisional = {}
        claimed = set(direct_addresses)
        pending = [function for function, row in zip(functions, direct_rows) if row is None]
        while pending:
            progress = False
            for function in list(pending):
                same = [row for row in remaining_rows if int(row['address'], 0) not in claimed
                        and row['bytes'] == function['size']]
                if len(same) == 1:
                    provisional[id(function)] = same[0]
                    claimed.add(int(same[0]['address'], 0))
                    pending.remove(function)
                    progress = True
            if not progress:
                break
        for function in functions:
            row = direct_row(function)
            if row is None:
                row = provisional.get(id(function))
            if row is None:
                remaining = [item for item in source_rows
                             if int(item['address'], 0) not in used_addresses]
                same_size = [item for item in remaining if item['bytes'] == function['size']]
                if len(same_size) == 1:
                    row = same_size[0]
                elif len(remaining) == 1 and remaining[0]['bytes'] >= function['size']:
                    row = remaining[0]
                elif order_pair and remaining:
                    row = remaining[0]
            if row is None:
                stats['unmatchedFunctions'] += 1
                continue
            address = int(row['address'], 0)
            used_addresses.add(address)
            target_size = row['bytes']
            measured_size = min(function['size'], target_size)
            if measured_size <= 0:
                continue
            function['address'] = address
            patched, unresolved = patch_function(function, module, base, profile['sections'],
                                                 profile['relocations'], image)
            stats['unresolvedRelocations'] += len(unresolved)
            start = address - base
            target = image[start:start + measured_size]
            exact = len(patched) >= measured_size and patched[:measured_size] == target
            item = dict(module=record['module'], start=address, end=address + measured_size,
                        source=record['source'], function=function['name'], mode=function['mode'],
                        size=measured_size, bytes=patched[:measured_size], exact=exact, unresolved=len(unresolved))
            stats['mappedFunctions'] += 1
            stats['exactFunctions'] += int(exact)
            bucket = selections[record['module']]
            previous = bucket.get(address)
            if previous is None:
                bucket[address] = item
            elif exact and not previous['exact']:
                bucket[address] = item
            elif exact and previous['exact'] and previous['bytes'] != item['bytes']:
                stats['duplicateAddresses'] += 1
            elif not exact and not previous['exact']:
                stats['duplicateAddresses'] += 1
    return ({name: [value for unused_address, value in sorted(values.items())]
             for name, values in selections.items()}, stats, report)


def check_spans(selected, data, base, limit, name):
    cursor = base
    for item in sorted(selected, key=lambda value: value['start']):
        if item['start'] < cursor or item['end'] <= item['start'] or item['end'] > limit:
            raise RepositoryBuildError('Overlapping or escaping compiled spans: ' + name)
        cursor = item['end']
    cursor = base
    for item in sorted(data, key=lambda value: value['start']):
        if item['start'] < cursor or item['end'] <= item['start'] or item['end'] > limit:
            raise RepositoryBuildError('Overlapping or escaping typed-data spans: ' + name)
        cursor = item['end']


def nonoverlapping(rows):
    result = []
    cursor = 0
    for row in sorted(rows, key=lambda value: value['start']):
        if row['start'] < cursor:
            continue
        result.append(row)
        cursor = row['end']
    return result


def git_revision(root):
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()


def build_project(root, private_root, out_dir, compilation):
    root, private, out_dir = Path(root).resolve(), Path(private_root).resolve(), Path(out_dir).resolve()
    if not out_dir.is_relative_to(root / 'build') and not out_dir.is_relative_to(root / 'work'):
        raise RepositoryBuildError('Generated project must remain beneath build/ or work/')
    config = load_config(root)
    modules = module_inventory(root, config)
    images = image_cache(root, modules)
    selections, stats, report = compiled_selections(root, private, compilation)
    data = accepted_data(root, config['data'].get('buildSha256'))
    by_address, unused_by_symbol, unused_source, unused_count = ledger_index(private)
    selected_functions = sum(len(value) for value in selections.values())
    units = []
    matched_code = matched_data = total_code = total_data = complete_functions = 0
    out_dir.mkdir(parents=True, exist_ok=True)
    elf_object(out_dir / 'base/empty.o', b'', [], True)
    for name, module in modules.items():
        base = int(module['loadAddressBase'], 0)
        image = images[name]
        category = ('child_' if module.get('program') else 'host_') + module['processor']
        physical = ('child' if module.get('program') else 'host') + '/' + module['processor'] + '/' + name
        selected = selections.get(name, [])
        source_data = data.get(name, [])
        check_spans(selected, source_data, base, base + len(image), name)
        sections = original_sections(root, name, module)
        candidates = []
        for (module_name, address), row in by_address.items():
            if module_name != name:
                continue
            size = row.get('bytes')
            if type(size) is not int or size <= 0 or address < base or address + size > base + len(image):
                continue
            if any(item['start'] < address + size and address < item['end'] for item in selected):
                continue
            if any(item['start'] < address + size and address < item['end'] for item in source_data):
                continue
            if any(address < stop and start < address + size and (not code or start > address or stop < address + size)
                   for start, stop, code in sections):
                continue
            candidates.append(dict(start=address, end=address + size, symbol=row['symbol'],
                                   mode=row.get('mode', 'data')))
        candidates = nonoverlapping(candidates)
        points = {base, base + len(image)}
        for item in selected:
            points.update((item['start'], item['end']))
        for begin, end, unused_code in sections:
            points.update(value for value in (begin, end) if base < value < base + len(image))
        for row in candidates:
            points.update((row['start'], row['end']))
        for item in source_data:
            points.update((item['start'], item['end']))
        ordered = sorted(points)
        for begin, end in zip(ordered, ordered[1:]):
            selection = next((item for item in selected if item['start'] <= begin and end <= item['end']), None)
            data_span = next((item for item in source_data if item['start'] <= begin and end <= item['end']), None)
            candidate = next((item for item in candidates if item['start'] == begin and item['end'] == end), None)
            known = next((code for start, stop, code in sections if start <= begin and end <= stop), None)
            if data_span and (selection or candidate):
                raise RepositoryBuildError('Qualified initialized data overlaps measured code: ' + name)
            code = bool(selection or candidate)
            payload = image[begin - base:end - base]
            if selection:
                source = selection['source']
                symbols = [(selection['function'], begin - selection['start'], end - begin, selection['mode'])]
                payload = selection['bytes'][begin - selection['start']:end - selection['start']]
                complete = selection['exact'] and len(payload) == end - begin
                if complete:
                    matched_code += end - begin
                    complete_functions += 1
            elif candidate:
                source = 'src'
                symbols = [(candidate['symbol'], 0, end - begin, candidate['mode'])]
                complete = False
            elif data_span:
                source = data_span['source']
                symbols = [(data_span.get('symbol') or f'__source_data_{begin:08x}', 0, end - begin, 'data')]
                complete = True
                matched_data += end - begin
            else:
                source = 'src'
                if not code and known is not False:
                    symbols = [(f'__initialized_span_{begin:08x}', 0, end - begin, 'data')]
                else:
                    symbols = []
                complete = False
            if code:
                total_code += end - begin
            else:
                total_data += end - begin
            key = hashlib.sha256((physical + '/' + str(begin)).encode()).hexdigest()[:20]
            target_path = out_dir / 'target' / (key + '.o')
            base_path = out_dir / 'base' / (key + '.o')
            elf_object(target_path, image[begin - base:end - base], symbols, code)
            metadata = dict(source_path=source, complete=complete, progress_categories=[category])
            if not code and not data_span and known is not False:
                metadata['progress_categories'].append('unclassified')
            group = str(PurePosixPath(source).with_suffix('')) if selection or data_span else 'unreconstructed'
            item = dict(name=group + '/' + physical + f'/{begin:08x}',
                        target_path=target_path.relative_to(out_dir).as_posix(),
                        base_path='base/empty.o', metadata=metadata)
            if selection or data_span:
                elf_object(base_path, payload, symbols, code)
                item['base_path'] = base_path.relative_to(out_dir).as_posix()
            units.append(item)
    if not units:
        raise RepositoryBuildError('No objdiff units were generated')
    if total_code + total_data != DENOMINATOR:
        raise RepositoryBuildError('Project units do not cover the initialized denominator')
    if matched_code + matched_data > DENOMINATOR:
        raise RepositoryBuildError('Matched units exceed the initialized denominator')
    project = dict(min_version='3.8.3', build_base=False, build_target=False, units=units,
                   progress_categories=CATEGORIES)
    write(out_dir / 'objdiff.json', project)
    functional = []
    draft_path = private / 'ledger/behavior-drafts-20261101.json'
    if draft_path.is_file():
        accepted_addresses = {(module, item['start']) for module, rows in selections.items() for item in rows}
        for row in read_json(draft_path).get('functions', []):
            state = row.get('states', {})
            if state.get('boundedBehaviorQualified') is True and not state.get('functionMatched'):
                address = int(row['address'], 0)
                if (row['module'], address) not in accepted_addresses:
                    name = row.get('symbol') or row.get('name')
                    if not name:
                        ledger_row = by_address.get((row['module'], address))
                        name = ledger_row['symbol'] if ledger_row else None
                    if name:
                        functional.append(dict(name=name, confidence='medium'))
    write(out_dir / 'functional.json', dict(functions=sorted(functional, key=lambda item: item['name'])))
    summary = dict(
        schemaVersion=1, publicGitRevision=git_revision(root), diagnostic=False, publishable=True,
        denominator=DENOMINATOR, moduleCount=len(modules),
        totalCodeBytes=total_code, totalDataBytes=total_data,
        acceptedFunctionCodeBytes=matched_code, matchedTypedDataBytes=matched_data,
        matchedCodeBytes=matched_code, acceptedFunctions=complete_functions,
        selectedFunctions=selected_functions, units=len(units),
        compileFailures=stats['compileFailures'], compiledObjects=stats['compiledObjects'],
        mappedFunctions=stats['mappedFunctions'], exactFunctions=stats['exactFunctions'],
        unmatchedFunctions=stats['unmatchedFunctions'], duplicateAddresses=stats['duplicateAddresses'],
        unresolvedRelocations=stats['unresolvedRelocations'], runtimeSymbols=stats.get('runtimeSymbols', 0),
        sourceUnitConfigSha256=digest(root / CONFIG),
        accounting='Compiled source is compared byte-for-byte with the original module image after applying its '
                   'ELF relocations. complete is true only for an exact, full-size match; no manifest membership '
                   'is used. Typed data remains the separately measured accepted-data budget.',
    )
    write(out_dir / 'export-receipt.json', summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description='Compile every resolved source file and build the objdiff project.')
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--private-root', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, default=Path('build/B2JJ-modified'))
    parser.add_argument('--compile-report', type=Path, default=Path('build/repository-compile/report.json'))
    parser.add_argument('--compile-only', action='store_true')
    parser.add_argument('--project-only', action='store_true')
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--source', action='append', default=[])
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    compile_report = args.compile_report if args.compile_report.is_absolute() else root / args.compile_report
    try:
        if not args.project_only:
            report = compile_all(root, args.private_root, compile_report.parent, args.jobs, limit=args.limit,
                                 sources=args.source)
            print(json.dumps({key: report[key] for key in ('status', 'selectedCompilationUnits', 'compiledUnits',
                                                           'failedUnits', 'fullRepositoryCompiled')}))
            if args.compile_only:
                return 0
        summary = build_project(root, args.private_root, output, compile_report)
        print(json.dumps(summary, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, struct.error) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
