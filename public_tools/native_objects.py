import copy
import hashlib
import json
import os
import re
import struct
import subprocess
from pathlib import Path
from bytematch_project import compile_index, contained, digest, read, write
from compile_sources import compiler_index
from public_manifest import compiler_flags
from native_mb_context import local_bss_profile


def object_contract(path):
    raw = Path(path).read_bytes()
    if raw[:7] != b'\x7fELF\x01\x01\x01':
        raise ValueError('Expected a fresh relocatable ARM ELF32 object')
    header = struct.unpack_from('<16sHHIIIIIHHHHHH', raw)
    if header[1:4] != (1, 40, 1) or header[11] != 40:
        raise ValueError('Expected a fresh relocatable ARM ELF32 object')
    sections = [struct.unpack_from('<IIIIIIIIII', raw, header[6] + 40 * i) for i in range(header[12])]
    def body(section):
        if section[4] + section[5] > len(raw):
            raise ValueError('Source ELF section escapes its object')
        return raw[section[4]:section[4] + section[5]]
    def string(strings, offset):
        end = strings.find(b'\0', offset)
        if offset < 0 or end < 0:
            raise ValueError('Invalid source ELF string')
        return strings[offset:end].decode('utf-8')
    names = body(sections[header[13]])
    allocated = {i: n for n, i in enumerate(i for i, s in enumerate(sections) if s[2] & 2)}
    tables = {}
    for index, section in enumerate(sections):
        if section[1] != 2:
            continue
        strings = body(sections[section[6]])
        table = []
        for offset in range(0, section[5], 16):
            symbol = struct.unpack_from('<IIIBBH', body(section), offset)
            table.append((string(strings, symbol[0]), *symbol[1:]))
        tables[index] = table
    result = []
    for index in allocated:
        section = sections[index]
        definitions = sorted((s[0], s[1], s[2], s[3], s[4]) for table in tables.values() for s in table
                             if s[5] == index and s[3] & 15 != 4)
        relocations = []
        for reloc in sections:
            if reloc[1] not in (4, 9) or reloc[7] != index:
                continue
            step = 12 if reloc[1] == 4 else 8
            for offset in range(0, reloc[5], step):
                address, info = struct.unpack_from('<II', body(reloc), offset)
                symbol = tables[reloc[6]][info >> 8]
                target = ('allocated', allocated[symbol[5]]) if symbol[5] in allocated else ('special', symbol[5])
                addend = struct.unpack_from('<i', body(reloc), offset + 8)[0] if step == 12 else None
                relocations.append((address, info & 255, symbol[:5], target, addend))
        payload = 'zero-fill' if section[1] == 8 else hashlib.sha256(body(section)).hexdigest()
        result.append((string(names, section[0]), section[1], section[2], section[5], section[8], section[9],
                       payload, tuple(definitions), tuple(sorted(relocations))))
    if not result:
        raise ValueError('Source object has no allocated sections')
    return header[7], tuple(result)


def safe_flags(root, values):
    result, pending = [], []
    for value in values:
        if re.fullmatch(r'-D[A-Za-z_]\w*(?:=[A-Za-z0-9_+.-]+)?', value):
            if pending:
                result.extend(compiler_flags(root, pending)[0])
                pending = []
            result.append(value)
        else:
            pending.append(value)
    if pending:
        result.extend(compiler_flags(root, pending)[0])
    return result


def selected_metadata(root, canonical, program=None, processor=None):
    names = {m['module'] for m in canonical['modules'] if m.get('processor', processor) == processor}
    units = [u for u in canonical['sourceUnits'] if u['module'] in names]
    def key(item, canonical_unit=False):
        begin = int(item['start'] if canonical_unit else item['address'], 0)
        size = int(item['end'], 0) - begin if canonical_unit else item.get('bytes', item.get('size'))
        return item['module'], begin, size, item['source'].replace('\\', '/'), item['sourceSha256']
    expected = {key(unit, True): unit for unit in units}
    sources = {(u['source'].replace('\\', '/'), u['sourceSha256']) for u in units}
    registry = read(contained(root, 'recovery.json'))['batches']
    report_names = {b['report'] for b in registry}
    preferred = {}
    for row in read(contained(root, 'public/accepted-functions.json'))['functions']:
        identity = (row['module'], int(row['address'], 0), row['bytes'], row['sourceUnit'], row['sourceSha256'])
        if row.get('evidence') in report_names:
            preferred[identity] = row['evidence']
    for row in read(contained(root, 'public/accepted-data.json'))['records']:
        identity = (row['module'], int(row['address'], 0), row['bytes'], row['source'].replace('\\', '/'), row['sourceSha256'])
        if row.get('evidence') in report_names:
            preferred[identity] = row['evidence']
    selected, metadata, symbols, bindings = {}, {}, {}, {}
    needed = {name.removeprefix('__native_entry_') for u in units for name in u.get('nativeEntryAliases', [])}
    needed.update(r['name'].removeprefix('__native_entry_') for m in canonical['modules']
                  if m['module'] in names for r in m.get('originalGapFunctionBindings', []))
    def binding_rows(value):
        if isinstance(value, dict):
            return [dict(row, name=row.get('name', name)) for name, row in value.items() if isinstance(row, dict)]
        return [row for row in value if isinstance(row, dict) and row.get('name')] if isinstance(value, list) else []
    def add_binding(binding):
        if program is None or (binding.get('program') or None) != program or binding.get('processor', processor) != processor:
            return
        physical = lambda b: ((b.get('program') or None), b.get('processor', processor), b.get('module'),
                              b.get('kind'), b.get('mode'), int(b['address'], 0))
        previous = bindings.setdefault(binding['name'], binding)
        if physical(previous) != physical(binding):
            raise ValueError('Conflicting selected physical native binding: ' + binding['name'])
        if binding['name'] in symbols and int(symbols[binding['name']], 0) != int(binding['address'], 0):
            raise ValueError('Conflicting selected native binding address')
        symbols[binding['name']] = binding['address']
    for batch in registry:
        pins = {(name.replace('\\', '/'), value) for name, value in batch.get('sourceHashes', {}).items()}
        if not sources.intersection(pins) and batch.get('kind') not in ('container', 'mixed'):
            continue
        report = read(contained(root, batch['report']))
        if (report.get('program') or None) != program:
            continue
        if report.get('romSha256') != canonical['buildNamespace']:
            raise ValueError('Frozen metadata belongs to another measured build')
        if program is None:
            if report.get('processor') != processor and not report.get('module', '').startswith('arm7'):
                continue
        elif report.get('processor') not in (None, processor):
            continue
        for name, value in report.get('nativeSymbols', {}).items():
            if name in symbols and int(symbols[name], 0) != int(value, 0):
                raise ValueError('Conflicting frozen native binding: ' + name)
            symbols[name] = value
        groups = [(e, 'function') for e in report.get('functionMatches', report.get('matches', report.get('functions', [])))]
        groups += [(e, 'data') for e in report.get('dataMatches', [])]
        groups += [(e, 'container') for e in report.get('containerMatches', [])]
        groups += [(e, 'linkage') for e in report.get('linkageMatches', [])]
        for entry, kind in groups:
            item = {**report, **entry}
            if (item.get('program') or None) != program:
                continue
            if processor is not None and item.get('processor', processor) != processor:
                continue
            if kind == 'container':
                metadata[(item['source'], item.get('name'), item.get('processor'))] = item
                continue
            identity = key(item)
            if identity not in expected:
                continue
            if identity in preferred and preferred[identity] != batch['report']:
                continue
            unit = expected[identity]
            if kind == 'linkage':
                item.update(kind='linkage', mode=item['entryMode'])
                if item.get('ordinaryFunctionCredit') != 0:
                    raise ValueError('Frozen linkage has source credit')
            elif not (item.get('exactBytes') or item.get('exactAfterDeclaredRelocation') or item.get('kind') == 'bss' and item.get('exactZeroStorage')):
                continue
            name = unit.get('function') or unit.get('symbol')
            if name and item.get('name') != name:
                continue
            relocations = item.get('relocations', [])
            if isinstance(relocations, list):
                needed.update(r['symbol'] for r in relocations if isinstance(r, dict) and r.get('symbol'))
            for binding in binding_rows(entry.get('nativeSymbolBindings', [])):
                add_binding(binding)
            item['canonicalObject'] = unit['object']
            item['canonicalObjectSha256'] = unit['sha256']
            item['frozenMetadataReport'] = batch['report']
            previous = selected.get(identity)
            if previous is None or item.get('objectSha256') == unit['sha256']:
                selected[identity] = item
        for binding in binding_rows(report.get('nativeSymbolBindings', [])):
            if binding['name'] in needed:
                add_binding(binding)
    if set(selected) != set(expected):
        missing = sorted(set(expected) - set(selected))
        raise ValueError('Frozen selected metadata is incomplete: ' + str(missing[:3]))
    return list(selected.values()), symbols, list(bindings.values()), list(metadata.values())


class FreshObjects:
    def __init__(self, root, compilation, output, compiler_root, license_file, runner=subprocess.run):
        self.root, self.output = root.resolve(), output.resolve()
        if not self.output.is_relative_to(self.root / 'work'):
            raise ValueError('Auxiliary compiler outputs must remain under work/')
        self.manifest_path = contained(self.root, 'public/accepted-functions.json')
        self.manifest = read(self.manifest_path)
        self.data = read(contained(self.root, 'public/accepted-data.json'))['records']
        self.compilation = contained(self.root, compilation)
        self.fresh = compile_index(self.root, self.compilation, digest(self.manifest_path))
        self.compiler_root, self.license_file = compiler_root.resolve(), license_file.resolve()
        self.compilers, self.pins, self.contracts, self.records = {}, {}, {}, []
        self.unavailable = set()
        for name in ('public/accepted-functions.json', 'public/accepted-data.json'):
            self.pins[contained(self.root, name)] = digest(contained(self.root, name))
        self.pins[self.compilation] = digest(self.compilation)
        for row in read(self.compilation)['results']:
            self.pins[contained(self.root, row['object'])] = row['objectSha256']
        self.runner = runner

    def pin(self, name, expected):
        path = contained(self.root, name)
        if path not in self.pins:
            self.pins[path] = digest(path)
        if self.pins[path] != expected:
            raise ValueError('Frozen native build input differs: ' + str(name))
        return path

    def profile(self, unit):
        local = local_bss_profile(unit, self.manifest)
        if local is not None:
            return local
        source = unit['source'].replace('\\', '/')
        begin, end = int(unit['start'], 0), int(unit['end'], 0)
        if unit.get('kind', 'function') == 'function':
            rows = [r for r in self.manifest['functions'] if r['module'] == unit['module'] and r['sourceUnit'] == source
                    and r['sourceSha256'] == unit['sourceSha256'] and begin <= int(r['address'], 0) < end]
            cursor = begin
            for row in sorted(rows, key=lambda r: int(r['address'], 0)):
                if int(row['address'], 0) != cursor:
                    raise ValueError('Canonical native unit is outside the closed function snapshot')
                cursor += row['bytes']
            if cursor != end:
                raise ValueError('Canonical native unit is outside the closed function snapshot')
        else:
            rows = [r for r in self.data if r['module'] == unit['module'] and r['source'].replace('\\', '/') == source
                    and r['sourceSha256'] == unit['sourceSha256'] and int(r['address'], 0) == begin and r['bytes'] == end - begin]
        profiles = {(r['compilerSha256'], tuple(r['compilerFlags'])) for r in rows}
        if len(profiles) != 1:
            raise ValueError('Canonical native unit lacks one closed compiler profile: ' + source)
        compiler, flags = profiles.pop()
        return source, compiler, flags

    def compile(self, key, dependencies):
        source_name, compiler_hash, flags = key
        if key in self.fresh:
            return self.fresh[key]
        source = contained(self.root, source_name)
        if source.suffix.lower() not in {'.c', '.cpp', '.cc', '.s'} or source_name.split('/')[0] not in {'src', 'generated'}:
            raise ValueError('Auxiliary source must be pinned authored or generated C/assembly')
        for row in dependencies:
            self.pin(row['path'], row['sha256'])
        if compiler_hash not in self.compilers:
            self.compilers.update(compiler_index(self.compiler_root, {compiler_hash}))
        compiler = self.compilers[compiler_hash]
        self.pin(compiler.relative_to(self.root).as_posix(), compiler_hash)
        directory = self.output / hashlib.sha256(json.dumps(key).encode()).hexdigest()[:20]
        directory.mkdir(parents=True, exist_ok=True)
        obj = directory / 'fresh.o'
        if obj.exists():
            obj.unlink()
        options = safe_flags(self.root, list(flags))
        if '-c' not in options:
            options.append('-c')
        command = [str(compiler), *options, str(source), '-o', str(obj)]
        environment = dict(os.environ, LM_LICENSE_FILE=str(self.license_file))
        result = self.runner(command, cwd=self.root, env=environment, capture_output=True, timeout=90)
        (directory / 'compiler.log').write_bytes(result.stdout + result.stderr)
        if result.returncode or not obj.is_file():
            raise ValueError('Fresh auxiliary compilation failed: ' + source_name)
        object_contract(obj)
        self.fresh[key] = obj
        self.pins[obj] = digest(obj)
        self.records.append(dict(source=source_name, compilerSha256=compiler_hash, compilerFlags=list(flags),
                                 sourceSha256=digest(source), sourceDependencies=dependencies,
                                 object=obj.relative_to(self.root).as_posix(), objectSha256=digest(obj),
                                 command=command, status='freshly-compiled'))
        return obj

    def replace(self, item, key):
        result = copy.deepcopy(item)
        source = self.pin(item['source'], item['sourceSha256'])
        for row in item.get('sourceDependencies', []):
            self.pin(row['path'], row['sha256'])
        original_name = item['object']
        original_hash = item.get('objectSha256', item.get('sha256'))
        fresh = self.compile(key, item.get('sourceDependencies', []))
        original = None
        candidates = [(original_name, original_hash)]
        if item.get('canonicalObject'):
            candidates.append((item['canonicalObject'], item['canonicalObjectSha256']))
        for name, expected in candidates:
            candidate = (self.root / name.replace('\\', '/')).resolve()
            if candidate.is_relative_to(self.root) and candidate.is_file() and digest(candidate) == expected:
                original = self.pin(name, expected)
                break
        if original is not None:
            contract_key = (original, fresh)
            if contract_key not in self.contracts:
                self.contracts[contract_key] = object_contract(original) == object_contract(fresh)
            if not self.contracts[contract_key]:
                raise ValueError('Fresh allocated source sections, symbols, or relocations differ: ' + str(source))
        else:
            self.unavailable.add((original_name, original_hash))
            object_contract(fresh)
        result['originalObject'] = original_name
        result['originalObjectSha256'] = original_hash
        result['object'] = fresh.relative_to(self.root).as_posix()
        result['objectSha256'] = digest(fresh)
        if 'sha256' in result and 'objectSha256' not in item:
            result['sha256'] = result['objectSha256']
        result['freshCompilationVerified'] = True
        result['historicalObjectVerified'] = original is not None
        result['nativeByteVerificationRequired'] = True
        return result

    def unit(self, unit):
        return self.replace(unit, self.profile(unit))

    def entry(self, item):
        if item.get('kind') == 'linkage':
            if item.get('ordinaryFunctionCredit') != 0:
                raise ValueError('Imported linkage must receive zero source function credit')
            self.pin(item['object'], item['objectSha256'])
            result = copy.deepcopy(item)
            result['importedFrozenLinkage'] = True
            return result
        if not item.get('compilerSha256') or not item.get('compilerFlags'):
            raise ValueError('Native entry lacks its original compiler profile')
        key = (item['source'].replace('\\', '/'), item['compilerSha256'], tuple(item['compilerFlags']))
        if item.get('module'):
            probe = dict(item, start=item['address'], end=hex(int(item['address'], 0) + item.get('bytes', item.get('size'))))
            if item.get('kind') not in ('bss', 'data', 'rodata', 'initialized-data'):
                probe['kind'] = 'function'
            if self.profile(probe) != key:
                raise ValueError('Native entry profile differs from the closed snapshot')
        return self.replace(item, key)

    def finish(self):
        if any(digest(path) != expected for path, expected in self.pins.items()):
            raise ValueError('Frozen inputs changed during focused native build')
        summary = dict(auxiliaryFreshCompilationUnits=len(self.records), equivalentObjectPairs=len(self.contracts),
                       unavailableHistoricalObjects=len(self.unavailable),
                       originalInputFilesChecked=len(self.pins), originalInputFilesUnchanged=True,
                       results=self.records)
        write(self.output / 'report.json', summary)
        return summary
