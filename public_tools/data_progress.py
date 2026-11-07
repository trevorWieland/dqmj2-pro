import re
import struct
from pathlib import Path, PurePosixPath

from build_receipts import DENOMINATOR, REPORTS, digest, pinned_file, read
from public_manifest import include_names


DATA_RECORDS = 450
DATA_BYTES = 109484
DATA_KINDS = {'data', 'rodata', 'initialized-data'}
GENERATED_VISIBILITY_COUNTS = {'public': 10, 'private-asset': 46}


def contained(root, name):
    if not isinstance(name, (str, Path)):
        raise ValueError('Missing typed-data input path')
    path = (root / str(name).replace('\\', '/')).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('Typed-data input is missing or escapes its checkout')
    return path


def source_name(name):
    if not isinstance(name, str):
        raise ValueError('Typed-data source path is missing')
    name = name.replace('\\', '/')
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or ':' in name or path.as_posix() != name:
        raise ValueError('Typed-data source path must remain repository-relative')
    return name


def profile(row):
    flags = row.get('compilerFlags')
    if not isinstance(flags, list) or not flags or any(not isinstance(flag, str) for flag in flags):
        raise ValueError('Typed-data compiler flags are missing')
    compiler = row.get('compilerSha256')
    if not isinstance(compiler, str) or not re.fullmatch(r'[0-9a-f]{64}', compiler):
        raise ValueError('Typed-data compiler identity is missing')
    return source_name(row['source']), compiler, tuple(flags)


def object_symbol(path, wanted, size):
    raw = path.read_bytes()
    if raw[:7] != b'\x7fELF\x01\x01\x01' or len(raw) < 52:
        raise ValueError('Fresh typed-data object is not ARM ELF32')
    header = struct.unpack_from('<16sHHIIIIIHHHHHH', raw)
    if header[1:4] != (1, 40, 1) or header[11] != 40:
        raise ValueError('Fresh typed-data object must be relocatable ARM ELF32')
    if header[6] + header[12] * 40 > len(raw):
        raise ValueError('Typed-data ELF section table escapes its object')
    sections = [struct.unpack_from('<IIIIIIIIII', raw, header[6] + i * 40) for i in range(header[12])]
    choices = []
    for section in sections:
        if section[1] != 2:
            continue
        if section[9] != 16 or section[5] % 16 or section[6] >= len(sections):
            raise ValueError('Typed-data ELF symbol table is invalid')
        strings = sections[section[6]]
        if section[4] + section[5] > len(raw) or strings[4] + strings[5] > len(raw):
            raise ValueError('Typed-data ELF symbol payload escapes its object')
        text = raw[strings[4]:strings[4] + strings[5]]
        for offset in range(section[4], section[4] + section[5], 16):
            name_at, value, symbol_size, info, unused_other, index = struct.unpack_from('<IIIBBH', raw, offset)
            end = text.find(b'\0', name_at)
            if end < 0:
                raise ValueError('Typed-data ELF symbol name is invalid')
            name = text[name_at:end].decode('utf-8')
            if name != wanted:
                continue
            if info & 15 != 1 or not 0 < index < len(sections) or symbol_size != size:
                raise ValueError('Typed-data source symbol is not the complete initialized object')
            target = sections[index]
            if target[1] != 1 or not target[2] & 2 or value + size > target[5]:
                raise ValueError('Typed-data source symbol leaves initialized allocated storage')
            choices.append(name)
    if len(choices) != 1:
        raise ValueError('Typed-data source object symbol is absent or ambiguous')
    return choices[0]


def load_data_spans(root, private, verified_build):
    if not verified_build or verified_build.get('buildScope') != 'native-modules':
        return {}
    root, private = Path(root).resolve(), Path(private).resolve()
    if private != root:
        raise ValueError('Typed-data progress requires materialized native inputs in the public checkout')
    native, outer = verified_build['nativeReceipt'], verified_build['receipt']
    if native.get('nativeBuildPassed') is not True or native.get('allModuleBytesExact') is not True or native.get('allSymbolChecksPassed') is not True:
        raise ValueError('Typed-data progress requires successful genuine native module links')
    native_started, started = native['startedTimeNs'], outer['startedTimeNs']
    native_path = pinned_file(root, outer['nativeBuildReceipt'], native_started, 'Native build receipt')
    native_parent = native_path.parent
    if read(native_path) != native:
        raise ValueError('Verified native receipt changed before typed-data export')
    pins = {}
    def pin(name, expected):
        path = contained(root, name)
        if path not in pins:
            pins[path] = digest(path)
        if pins[path] != expected:
            raise ValueError('Frozen typed-data source, dependency, or object identity differs')
        return path
    manifest_path = root / 'public/accepted-functions.json'
    pin(manifest_path, native['acceptedManifestSha256'])
    manifest = read(manifest_path)
    data_path = contained(root, 'public/accepted-data.json')
    pins[data_path] = digest(data_path)
    data = read(data_path)
    if data.get('schemaVersion') != 1 or data.get('buildSha256') != manifest['romSha256']:
        raise ValueError('Typed-data and function snapshots name different builds')
    rows = []
    for row in data['records']:
        if row.get('kind') == 'bss':
            continue
        if row.get('kind') not in DATA_KINDS or row.get('states', {}).get('dataMatched') is not True or row.get('states', {}).get('moduleLinked') is not True:
            raise ValueError('Typed-data snapshot contains unqualified initialized source')
        if row.get('buildSha256') != manifest['romSha256'] or type(row.get('bytes')) is not int or row['bytes'] <= 0 or row.get('storedBytes') != row['bytes']:
            raise ValueError('Typed-data build identity or initialized extent differs')
        rows.append(row)
    if len(rows) != DATA_RECORDS or sum(row['bytes'] for row in rows) != DATA_BYTES:
        raise ValueError('The complete closed typed-data snapshot is required')
    wanted = {profile(row) for row in rows}
    compilation = pinned_file(root, outer['publicSourceCompileReport'], started, 'Source compilation report')
    if compilation != Path(verified_build['compilation']).resolve() or native.get('publicSourceCompileReport') != outer['publicSourceCompileReport']:
        raise ValueError('Typed-data source compilation differs from the verified native build')
    public_compilation = read(compilation)
    if public_compilation.get('status') != 'source-compilation-passed' or public_compilation.get('fullManifestCompiled') is not True or public_compilation.get('manifestSha256') != native['acceptedManifestSha256']:
        raise ValueError('Typed-data progress requires complete current source compilation')
    fresh = {}
    def index(records, status, not_before, auxiliary):
        for item in records:
            key = profile(item)
            if key not in wanted:
                continue
            if item.get('status') != status:
                raise ValueError('Typed-data compiler did not succeed')
            path = pin(item['object'], item['objectSha256'])
            if path.stat().st_mtime_ns < not_before or auxiliary and not path.is_relative_to(native_parent / 'fresh-auxiliary'):
                raise ValueError('Typed-data compiler object predates or escapes this native build')
            if key in fresh and fresh[key] != (path, item['objectSha256']):
                raise ValueError('Ambiguous fresh typed-data compiler profile')
            fresh[key] = path, item['objectSha256']
    index(public_compilation['results'], 'compiled', started, False)
    index(native['freshCompilation']['results'], 'freshly-compiled', native_started, True)
    inventory = read(contained(private, 'ledger/modules.json'))
    modules = {module['name']: module for module in inventory['modules']}
    if inventory['buildSha256'] != manifest['romSha256'] or len(modules) != 20 or sum(m['bytes'] for m in modules.values()) != DENOMINATOR:
        raise ValueError('Typed-data progress requires the complete measured native inventory')
    links, units = {}, {}
    for name in REPORTS:
        path = Path(verified_build['reports'][name]).resolve()
        relative = path.relative_to(root).as_posix()
        report_pin = dict(outer['reports'][relative], path=relative)
        pinned_file(root, report_pin, native_started, 'Native link report', native_parent / 'evidence/linking')
        report = read(path)
        if report.get('buildNamespace') != manifest['romSha256'] or report.get('allModuleBytesExact') is not True or report.get('symbolCheckPassed') is not True:
            raise ValueError('Typed-data native link report did not pass')
        for linked in report['modules']:
            module = modules[linked['module']]
            if linked['module'] in links or linked.get('exactBytes') is not True or linked['inputSha256'] != module['sha256'] or linked['outputSha256'] != module['sha256']:
                raise ValueError('Typed-data module link identity differs')
            original = pin(module['binary'], module['sha256'])
            output = pin(linked['output'], module['sha256'])
            if original.stat().st_size != module['bytes'] or output.stat().st_size != module['bytes'] or not output.is_relative_to(native_parent) or output.stat().st_mtime_ns < native_started:
                raise ValueError('Typed-data native output is incomplete or stale')
            links[linked['module']] = linked
        for unit in report['sourceUnits']:
            if unit.get('kind') not in DATA_KINDS:
                continue
            key = (unit['module'], int(unit['start'], 0), int(unit['end'], 0), source_name(unit['source']), unit['sourceSha256'])
            units.setdefault(key, []).append(unit)
    if set(links) != set(modules):
        raise ValueError('Typed-data progress omitted native module links')
    result, identities = {}, set()
    for row in rows:
        source = source_name(row['source'])
        if PurePosixPath(source).parts[0] not in {'src', 'generated'} or PurePosixPath(source).suffix != '.c':
            raise ValueError('Typed-data source_path must name its actual frozen C compiler input')
        pin(source, row['sourceSha256'])
        for dependency in row.get('sourceDependencies', []):
            pin(source_name(dependency['path']), dependency['sha256'])
        start, end = int(row['address'], 0), int(row['address'], 0) + row['bytes']
        module = modules[row['module']]
        if not int(module['base'], 0) <= start < end <= int(module['base'], 0) + module['bytes']:
            raise ValueError('Typed-data interval leaves its initialized module')
        key = (row['module'], start, end, source, row['sourceSha256'])
        matches = units.get(key, [])
        if len(matches) != 1 or matches[0].get('compiledBytes') != row['bytes']:
            raise ValueError('Typed-data interval lacks one exact canonical fresh linked source unit')
        unit = matches[0]
        if profile(row) not in fresh:
            raise ValueError('Typed-data source lacks fresh compiler provenance')
        fresh_path, fresh_hash = fresh[profile(row)]
        unit_path = pin(unit['object'], unit.get('objectSha256', unit.get('sha256')))
        if unit_path != fresh_path or any(unit.get(field, fresh_hash) != fresh_hash for field in ('sha256', 'objectSha256')):
            raise ValueError('Typed-data native link used an old or different compiler object')
        identity = row['module'], start, end
        if identity in identities:
            raise ValueError('Duplicate typed-data interval')
        identities.add(identity)
        span = dict(start=start, end=end, source=source, sourceSha256=row['sourceSha256'])
        symbol = unit.get('symbol') or unit.get('function')
        if symbol:
            span['symbol'] = object_symbol(fresh_path, symbol, row['bytes'])
        result.setdefault(row['module'], []).append(span)
    for spans in result.values():
        spans.sort(key=lambda row: row['start'])
        if any(previous['end'] > current['start'] for previous, current in zip(spans, spans[1:])):
            raise ValueError('Overlapping typed-data intervals')
    if any(digest(path) != expected for path, expected in pins.items()):
        raise ValueError('Typed-data source or native build inputs changed during export')
    return result


def check_public_data_sources(root):
    root = Path(root).resolve()
    data_path = contained(root, 'public/accepted-data.json')
    data = read(data_path)
    functions = read(contained(root, 'public/accepted-functions.json'))
    visibility = read(contained(root, 'public/data-source-visibility.json'))
    if (visibility.get('schemaVersion') != 1 or data.get('schemaVersion') != 1
            or visibility.get('snapshotRevision') != functions.get('revision')
            or data.get('buildSha256') != functions.get('romSha256')
            or visibility.get('acceptedDataManifestSha256') != digest(data_path)):
        raise ValueError('Public data visibility metadata is stale or has the wrong snapshot')
    namespaces = {}
    for row in functions['functions']:
        value = (row['processor'], row.get('program') or '')
        if namespaces.setdefault(row['module'], value) != value:
            raise ValueError('Ambiguous public data module namespace')
    rows = [row for row in data['records'] if row.get('kind') != 'bss']
    if any(row.get('kind') not in DATA_KINDS or row.get('states', {}).get('dataMatched') is not True
           or row.get('states', {}).get('moduleLinked') is not True for row in rows):
        raise ValueError('Public initialized data contains an unqualified record')
    generated = {row['id']: row for row in rows if source_name(row['source']).startswith('generated/')}
    declarations, counts = {}, dict.fromkeys(GENERATED_VISIBILITY_COUNTS, 0)
    for entry in visibility['sources']:
        identity, state = entry['id'], entry['visibility']
        if identity in declarations or identity not in generated or state not in counts:
            raise ValueError('Unknown, duplicate, or invalid generated data visibility')
        row = generated[identity]
        if (any(entry.get(field) != row.get(field) for field in ('source', 'sourceSha256', 'module', 'address'))
                or entry.get('initializedBytes') != row['bytes']
                or (entry.get('processor'), entry.get('program') or '') != namespaces.get(row['module'])
                or entry.get('cIncludeDependencies') != []
                or entry.get('generatorFamily') not in visibility['generators']):
            raise ValueError('Generated data visibility differs from its accepted source identity')
        allowed = {'mathematical-table', 'typed-sdk-table'} if state == 'public' else {'complete-encoded-game-asset'}
        if entry.get('classification') not in allowed:
            raise ValueError('Generated data visibility conflicts with its publication classification')
        declarations[identity] = entry
        counts[state] += 1
    if set(declarations) != set(generated) or counts != GENERATED_VISIBILITY_COUNTS:
        raise ValueError('Generated data visibility inventory is incomplete')
    pins, verified = {}, set()
    def pin(name, expected):
        path = contained(root, source_name(name))
        if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
            raise ValueError('Missing public typed-data source hash')
        if name in pins and pins[name] != expected:
            raise ValueError('Conflicting public typed-data source hashes')
        if name not in pins and digest(path) != expected:
            raise ValueError('Public typed-data source hash differs from its accepted declaration')
        pins[name] = expected
        return path
    for row in rows:
        declaration = declarations.get(row['id'])
        if declaration and declaration['visibility'] == 'private-asset':
            continue
        name = source_name(row['source'])
        if not name.startswith(('src/', 'generated/')) or Path(name).suffix != '.c':
            raise ValueError('Public typed-data source must be its actual C compiler input')
        source = pin(name, row['sourceSha256'])
        if declaration and (declaration.get('sourceTextBytes') != source.stat().st_size or include_names(source)):
            raise ValueError('Curated generated data is not the declared self-contained C file')
        dependencies = {name: source}
        for dependency in row.get('sourceDependencies', []):
            if Path(dependency['path']).suffix.lower() in {'.h', '.inc', '.inl'}:
                dependencies[dependency['path']] = pin(dependency['path'], dependency['sha256'])
        directories = [root]
        flags = row.get('compilerFlags', [])
        for index, flag in enumerate(flags[:-1]):
            if flag == '-i':
                folder = (root / flags[index + 1]).resolve()
                if not folder.is_relative_to(root):
                    raise ValueError('Public typed-data include directory escapes its checkout')
                directories.append(folder)
        for file in dependencies.values():
            for delimiter, include in include_names(file):
                if delimiter == '"':
                    resolved = next((candidate.resolve() for folder in [file.parent] + directories
                                     if (candidate := folder / include).is_file()), None)
                    if resolved not in dependencies.values():
                        raise ValueError('Public typed-data quoted include is outside its pinned C closure')
        verified.add(row['id'])
    generators = set()
    for family in visibility['generators'].values():
        for generator in family:
            name = source_name(generator['path'])
            if Path(name).suffix != '.py':
                raise ValueError('Public semantic generator path is not a Python source')
            pin(name, generator['sha256'])
            generators.add(name)
    if any(digest(root / name) != expected for name, expected in pins.items()):
        raise ValueError('Public typed-data inputs changed during verification')
    return dict(passed=True, publicDataRecordsVerified=len(verified), publicInitializedBytes=sum(
        row['bytes'] for row in rows if row['id'] in verified), publicGeneratedSourceFiles=counts['public'],
        privateAssetSourceFiles=counts['private-asset'], privateAssetSourcesRequired=False,
        publicSemanticGeneratorsVerified=len(generators), matchingCreditGranted=False)


def main():
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--check-public-sources', action='store_true', required=True)
    args = parser.parse_args()
    print(json.dumps(check_public_data_sources(args.root), sort_keys=True))


if __name__ == '__main__':
    main()
