"""Derive the committed source-unit rules from the private address ledger.

The build never runs this script.  It is the maintainer recipe that turns
``ledger/functions.jsonl`` (which records the accepted compiler profile of every
measured address) into a reviewable, public description of how to compile each
source directory.  Re-run it whenever a new source directory is merged without
an address in the ledger:

    python public_tools/derive_source_units.py \
        --root . --ledger ../dqmj2pro-decomp/ledger/functions.jsonl \
        --modules ../dqmj2pro-decomp/ledger/modules.json \
        --out config/source_units.json

Rules are inherited: a rule only needs to state the fields that differ from its
most specific ancestor.  The resolver in ``source_units.py`` merges the chain.
No function identity, function address or completion state is stored here.
"""

import argparse
import collections
import json
import posixpath
from pathlib import Path, PurePosixPath

SKIP_DIRECTORIES = {'nonmatching'}
TOP_LEVEL_FALLBACKS = {
    # The module a brand-new file directly beneath a top-level directory most
    # likely belongs to.  Directory-specific rules derived below override it.
    'arm7': 'arm7-main',
    'encounter': 'main',
    'hardware': 'main',
    'itcm': 'itcm',
    'main': 'main',
    'main_sdk_aux': 'main',
    'math': 'main',
    'mechanics_save': 'main',
    'nonmatching': None,
    'ov000': 'ov000',
    'ov001': 'ov001',
    'ov006': 'ov006',
    'overlays': 'ov001',
    'ports': 'main',
    'runtime': 'main',
    'scripts': 'main',
    'transplants': 'main',
    'utility': 'utility-child-arm9-main',
    'verified_assembly': 'main',
}
BASE_FLAGS = {
    'arm946e': ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e',
                '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off', '-RTTI', 'off',
                '-interworking', '-w', 'off', '-sym', 'on', '-gccinc', '-nolink', '-msgstyle', 'gcc'],
    'arm7tdmi': ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm7tdmi',
                 '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off', '-RTTI', 'off',
                 '-interworking', '-w', 'off', '-sym', 'on', '-gccinc', '-nolink', '-msgstyle', 'gcc'],
}
ARM946E_BASE = ['-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e', '-gccext,on',
                '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off', '-RTTI', 'off', '-interworking',
                '-w', 'off', '-sym', 'on', '-gccinc', '-nolink', '-msgstyle', 'gcc']
# Merged packet sources whose addresses exist in the ledger but whose accepted
# rows carry no compiler profile. These two profiles are the ones that reproduce
# the measured bytes; they are source-file rules, not function completions.
PACKET_PROFILE_OVERRIDES = {
    'src/ov001/p3_021d732c/021d75d4/native_ov001_021d75d4.c':
        (['-O4', *ARM946E_BASE], '6e253a8fcc9102a1b24ec0b4c856a89958bf693370792f06727c5b1e6cecab28'),
    'src/ov001/p3_021d732c/021d9270/native_ov001_021d9270.c':
        (['-O4,p', *ARM946E_BASE], '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'),
}


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def read_ledger(path):
    rows = []
    with Path(path).open(encoding='utf-8') as stream:
        for line in stream:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def source_files(root):
    result = []
    for path in (Path(root) / 'src').rglob('*.c'):
        relative = path.relative_to(root).as_posix()
        parts = PurePosixPath(relative).parts
        if any(part in SKIP_DIRECTORIES for part in parts):
            continue
        result.append(relative)
    return sorted(result)


def dominant(rows):
    counts = collections.Counter(
        ((row.get('program') or ''), row.get('processor'), row['module'], tuple(row.get('compilerFlags') or []),
         row.get('compilerSha256'))
        for row in rows)
    return counts.most_common(1)[0][0]


def compiler_inventory(root, compiler_root):
    import hashlib
    result = {}
    for path in sorted((Path(root) / compiler_root).rglob('mwccarm.exe')):
        identity = hashlib.sha256(path.read_bytes()).hexdigest()
        result.setdefault(identity, path.relative_to(root).as_posix())
    return result


def flags_of(row):
    return list(row.get('compilerFlags') or [])


def module_table(inventory):
    table = {}
    for module in inventory['modules']:
        image = module['binary'].replace('\\', '/')
        if not image.startswith('extract/'):
            raise ValueError('Module image is not an extracted binary: ' + image)
        table[module['name']] = dict(processor=module['processor'], loadAddressBase=module['base'],
                                     originalImage=image, bytes=module['bytes'],
                                     program=module.get('program'))
    return table


def flag_profile(profiles, flags):
    key = tuple(flags)
    if key not in profiles:
        profiles[key] = f'p{len(profiles):03d}'
    return profiles[key]


def build(root, ledger_path, modules_path, compiler, compiler_sha256, compiler_root):
    root = Path(root).resolve()
    inventory = read_json(modules_path)
    modules = module_table(inventory)
    compilers = compiler_inventory(root, compiler_root)
    if compiler_sha256 not in compilers:
        raise ValueError('Default compiler identity is absent from ' + compiler_root)
    rows = read_ledger(ledger_path)
    by_source = collections.defaultdict(list)
    for row in rows:
        name = row.get('sourceUnit')
        if isinstance(name, str) and name.endswith('.c'):
            by_source[name.replace('\\', '/')].append(row)
    files = source_files(root)
    known = {name: dominant(value) for name, value in by_source.items()}
    variants = collections.defaultdict(set)
    for name, value in by_source.items():
        for row in value:
            variants[name].add(((row.get('program') or ''), row.get('processor'), row['module'],
                                tuple(row.get('compilerFlags') or []), row.get('compilerSha256')))
    by_directory = collections.defaultdict(list)
    for name in known:
        by_directory[posixpath.dirname(name)].append(name)

    top_level = {}
    direct = []
    for name in known:
        parts = PurePosixPath(name).parts
        if len(parts) < 3:
            direct.append(name)
            continue
        top_level.setdefault(parts[1], []).append(name)
    ambiguity = sorted(name for name, values in variants.items() if len(values) > 1)

    rules = []
    profiles = {}

    def emit(glob, fields):
        rules.append(dict(glob=glob, **fields))

    def fields_for(module, flags, compiler_identity):
        fields = dict(module=module, compilerFlags=flag_profile(profiles, flags))
        if compiler_identity != compiler_sha256:
            fields['compilerSha256'] = compiler_identity
        return fields

    # One fallback per top-level directory so a newly merged subdirectory
    # inherits a complete module/profile instead of matching nothing.
    effective = {}
    existing = {path.name for path in (root / 'src').iterdir() if path.is_dir()}
    for top in sorted(existing | set(top_level)):
        if top == 'nonmatching':
            continue
        if top not in TOP_LEVEL_FALLBACKS:
            raise ValueError('No top-level fallback module for src/' + top)
        module = TOP_LEVEL_FALLBACKS[top]
        if module is None:
            continue
        processor = modules[module]['processor']
        variant = dominant([row for name in top_level[top] for row in by_source[name]]) if top in top_level else None
        if variant is not None and variant[1] == processor:
            fields = fields_for(module, variant[3], variant[4])
        else:
            fields = fields_for(module, BASE_FLAGS['arm946e' if processor == 'arm9' else 'arm7tdmi'], compiler_sha256)
        emit(f'src/{top}/**', fields)
        effective['src/' + top] = fields

    # Files directly beneath src/ get exact-path rules; there is deliberately no
    # src/** catch-all, so a new top-level directory must be classified.
    for name in sorted(direct):
        variant = known[name]
        emit(name, fields_for(variant[2], variant[3], variant[4]))
    for name in files:
        if name.count('/') != 1 or name in known:
            continue
        emit(name, fields_for('main', BASE_FLAGS['arm946e'], compiler_sha256))

    # Directory rules, parent before child. Only changed fields are emitted.
    all_directories = set(by_directory)
    for directory in list(by_directory):
        parent = posixpath.dirname(directory)
        while parent and parent != 'src':
            all_directories.add(parent)
            parent = posixpath.dirname(parent)
    for directory in sorted(all_directories, key=lambda value: (value.count('/'), value)):
        if directory == 'src' or directory in effective:
            continue
        parent = posixpath.dirname(directory)
        inherited = effective.get(parent, {})
        if directory not in by_directory:
            if directory not in effective:
                effective[directory] = inherited
            continue
        variant = dominant([row for name in by_directory[directory] for row in by_source[name]])
        own = fields_for(variant[2], variant[3], variant[4])
        if 'compilerSha256' in inherited and inherited['compilerSha256'] != variant[4]:
            own['compilerSha256'] = variant[4]
        changed = {key: value for key, value in own.items() if inherited.get(key) != value}
        if changed:
            emit(directory + '/**', changed)
            effective[directory] = {**inherited, **changed}
        else:
            effective[directory] = inherited

    # A file whose accepted profile differs from its directory rule gets an
    # exact-path override. These are flag variants inside an otherwise uniform
    # directory, not completions.
    overrides = 0
    for directory in sorted(by_directory):
        if directory == 'src':
            continue
        for name in sorted(by_directory[directory]):
            variant = known[name]
            own = fields_for(variant[2], variant[3], variant[4])
            inherited = effective.get(directory, {})
            if 'compilerSha256' in inherited and inherited['compilerSha256'] != variant[4]:
                own['compilerSha256'] = variant[4]
            changed = {key: value for key, value in own.items() if inherited.get(key) != value}
            if changed:
                emit(name, changed)
                overrides += 1

    for path, (flags, compiler_identity) in PACKET_PROFILE_OVERRIDES.items():
        fields = dict(compilerFlags=flag_profile(profiles, flags))
        if compiler_identity != compiler_sha256:
            fields['compilerSha256'] = compiler_identity
        emit(path, fields)

    rules.sort(key=lambda rule: (rule['glob'].count('/'), rule['glob']))
    alternates = {}
    used_compilers = {compiler_sha256}
    used_compilers.update(compiler for flags, compiler in PACKET_PROFILE_OVERRIDES.values())
    for values in variants.values():
        used_compilers.update(value[4] for value in values)
    compilers = {identity: path for identity, path in compilers.items() if identity in used_compilers}
    for name, values in sorted(variants.items()):
        if len(values) < 2:
            continue
        primary = known[name]
        others = sorted(values - {primary})
        if not others:
            continue
        alternates[name] = [
            dict(compilerFlags=flag_profile(profiles, flags),
                 **({} if compiler == compiler_sha256 else {'compilerSha256': compiler}))
            for unused_program, unused_processor, unused_module, flags, compiler in others]
    config = dict(
        schemaVersion=1,
        description='Compilation rules for every source directory. Rules inherit from their most specific ancestor rule; '
                    'the effective rule is completed from the module inventory and flag profiles. No function identities '
                    'or completion states are listed. Derived from the private address ledger.',
        denominator=sum(value['bytes'] for value in modules.values()),
        buildSha256=inventory['buildSha256'],
        exclusions=['src/nonmatching/**'],
        compiler=dict(path=compiler, sha256=compiler_sha256),
        compilers=compilers,
        modules={name: dict(processor=value['processor'], loadAddressBase=value['loadAddressBase'],
                            originalImage=value['originalImage'], bytes=value['bytes'], program=value['program'])
                 for name, value in sorted(modules.items())},
        flagProfiles={name: list(flags) for flags, name in sorted(profiles.items(), key=lambda item: item[1])},
        generatedFrom=dict(ledger='ledger/functions.jsonl', moduleInventory='ledger/modules.json',
                           sourceFiles=len(files), ledgerSourceFiles=len(known),
                           ambiguousSourceFiles=len(ambiguity), alternateProfiles=len(alternates)),
        alternates=alternates,
        rules=rules,
    )
    return config, files, known, ambiguity, overrides


def verify(config, root, files, known):
    """Confirm every source file under src/ resolves and every ledger profile survives."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from source_units import load_config, resolve, source_files, excluded

    loaded = load_config(None, config)
    all_files = source_files(root)
    unresolved = []
    resolved = excluded_count = 0
    for name in all_files:
        if excluded(loaded, name):
            excluded_count += 1
            continue
        try:
            resolve(loaded, name)
            resolved += 1
        except ValueError:
            unresolved.append(name)
    compiled = [name for name in files if not excluded(loaded, name)]
    wrong = []
    for name in compiled:
        if name not in known:
            continue
        rule = resolve(loaded, name)
        expected = known[name]
        if rule['module'] != expected[2] or tuple(rule['compilerFlags']) != expected[3] \
                or rule['compilerSha256'] != expected[4]:
            wrong.append(name)
    if unresolved:
        raise SystemExit('Unresolved sources: ' + ', '.join(unresolved[:10]))
    if wrong:
        raise SystemExit('Ledger profile differs for: ' + ', '.join(wrong[:10]))
    return dict(allFiles=len(all_files), resolvedFiles=resolved, excludedFiles=excluded_count,
                compiledSources=len(compiled))


def main():
    parser = argparse.ArgumentParser(description='Derive config/source_units.json from the private address ledger.')
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--modules', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path('config/source_units.json'))
    parser.add_argument('--compiler', default='tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
    parser.add_argument('--compiler-sha256',
                        default='7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880')
    parser.add_argument('--compiler-root', default='tools/mwccarm')
    args = parser.parse_args()
    config, files, known, ambiguity, overrides = build(args.root, args.ledger, args.modules,
                                                       args.compiler, args.compiler_sha256, args.compiler_root)
    out = args.out if args.out.is_absolute() else args.root / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(config, indent=1) + '\n', encoding='utf-8')
    checked = verify(config, args.root.resolve(), files, known)
    print(json.dumps(dict(output=out.name, rules=len(config['rules']), **checked,
                          ledgerSources=len(known), ambiguous=len(ambiguity),
                          overrides=overrides, bytes=out.stat().st_size)))


if __name__ == '__main__':
    main()
