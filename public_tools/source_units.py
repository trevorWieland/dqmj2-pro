"""Resolve every public source file to one compilation rule.

The committed ``config/source_units.json`` describes how to compile source
directories, not which functions are complete.  Rules inherit from their most
specific ancestor rule, so a new file merged into an existing directory is
compiled automatically.  A source file that matches no rule is a build error,
never a silent skip.

A lane may also declare its rules in ``config/rules.d/<lane>.json``, a JSON
array of the same rule objects.  Fragment files are loaded in filename order
before the base ``rules`` list and merged with it.  Resolution is unchanged:
the whole matching ancestor chain is merged from shallowest to deepest, so the
most specific glob wins.  Fragment globs are unique by construction; the
loader rejects a glob declared twice and names both sources.

Command line check used by CI and by ``derive_source_units.py``::

    python public_tools/source_units.py --root . --check
"""

import argparse
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath

CONFIG = 'config/source_units.json'
RULES_DIR = 'config/rules.d'
FIELDS = ('module', 'processor', 'compilerFlags', 'loadAddressBase', 'originalImage', 'mode')
RULE_FIELDS = FIELDS + ('compilerSha256',)
MODES = ('arm', 'thumb')
EXCLUSIONS = ('src/nonmatching/**',)
MODULES = {
    'main': 'arm9', 'itcm': 'arm9', 'dtcm': 'arm9', 'ov000': 'arm9', 'ov001': 'arm9',
    'ov002': 'arm9', 'ov003': 'arm9', 'ov004': 'arm9', 'ov005': 'arm9', 'ov006': 'arm9',
    'ov007': 'arm9', 'arm7-boot': 'arm7', 'arm7-wram': 'arm7', 'arm7-main': 'arm7',
    'utility-child-arm9-main': 'arm9', 'utility-child-arm9-itcm': 'arm9',
    'utility-child-arm9-dtcm': 'arm9', 'utility-child-arm7-boot': 'arm7',
    'utility-child-arm7-wram': 'arm7', 'utility-child-arm7-main': 'arm7',
}
ALLOWED_IMAGE_ROOTS = ('extract/', 'inputs/')


class SourceUnitError(ValueError):
    pass


def canonical(value):
    name = str(value).replace('\\', '/')
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or ':' in name or path.as_posix() != name:
        raise SourceUnitError('Source path must be repository-relative: ' + name)
    return name


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def rule_fragment_files(root):
    """The rule-fragment files for ``root``, in deterministic filename order."""
    directory = Path(root) / RULES_DIR
    if not directory.is_dir():
        return []
    return sorted((path for path in directory.glob('*.json') if path.is_file()),
                  key=lambda path: path.name)


def read_rule_fragments(root):
    """Read ``config/rules.d/*.json`` as ``[(origin, rules), ...]``.

    Each fragment is a JSON array of rule objects in the same shape as one
    entry of the base ``rules`` array.  Files are returned in filename order,
    so the merged configuration never depends on filesystem enumeration order.
    """
    fragments = []
    for path in rule_fragment_files(root):
        origin = RULES_DIR + '/' + path.name
        try:
            entries = read_json(path)
        except json.JSONDecodeError as error:
            raise SourceUnitError(f'Rule fragment {origin} is not valid JSON: {error}') from error
        if not isinstance(entries, list):
            raise SourceUnitError(f'Rule fragment {origin} must be a JSON array of source-unit rules')
        fragments.append((origin, entries))
    return fragments


def config_digest(root):
    """SHA-256 over the base configuration and every rule fragment.

    Rule fragments are part of the build configuration, so a compile report
    generated from one rule set must not validate against another.
    """
    root = Path(root).resolve()
    hasher = hashlib.sha256()
    for path in [root / CONFIG] + rule_fragment_files(root):
        hasher.update(path.relative_to(root).as_posix().encode('utf-8') + b'\0')
        hasher.update(path.read_bytes() + b'\0')
    return hasher.hexdigest()


def scope_of(glob):
    if not isinstance(glob, str) or not glob:
        raise SourceUnitError('A source-unit rule needs a glob')
    glob = canonical(glob)
    if glob == 'src/**':
        return 'src'
    if glob.endswith('/**'):
        return glob[:-3]
    if '*' in glob or '?' in glob or '[' in glob:
        raise SourceUnitError('Only directory globs (dir/**) or exact paths are supported: ' + glob)
    return glob


def depth(scope):
    return (scope.count('/'), len(scope))


def validate_flags(values, label='compilerFlags'):
    if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value for value in values):
        raise SourceUnitError(label + ' must be a nonempty string array')
    if '\\' in ' '.join(values):
        raise SourceUnitError(label + ' must not embed a path escape')
    return list(values)


def validate_rule(rule, modules):
    if not isinstance(rule, dict):
        raise SourceUnitError('Source-unit rules must be objects')
    scope = scope_of(rule.get('glob'))
    extra = set(rule) - {'glob', *RULE_FIELDS}
    if extra:
        raise SourceUnitError('Unsupported source-unit fields: ' + ', '.join(sorted(extra)))
    return dict(scope=scope, raw=rule)


def merge_chain(chain, modules, profiles, compilers, default_compiler):
    result = {}
    for rule in chain:
        for field in RULE_FIELDS:
            if field in rule:
                result[field] = rule[field]
    module = result.get('module')
    if module not in modules:
        raise SourceUnitError('Unknown or missing module in source-unit rule: ' + str(module))
    inventory = modules[module]
    result.setdefault('mode', 'arm')
    if result['mode'] not in MODES:
        raise SourceUnitError('Source-unit mode must be one of ' + ', '.join(MODES) + ': ' + str(result['mode']))
    result.setdefault('processor', inventory['processor'])
    result.setdefault('loadAddressBase', inventory['loadAddressBase'])
    result.setdefault('originalImage', inventory['originalImage'])
    result.setdefault('compilerSha256', default_compiler)
    profile = result.get('compilerFlags')
    if isinstance(profile, str):
        if profile not in profiles:
            raise SourceUnitError('Unknown compiler flag profile: ' + profile)
        result['compilerFlags'] = profiles[profile]
    missing = [field for field in FIELDS if field not in result]
    if missing:
        raise SourceUnitError('Source-unit rule chain is incomplete: ' + ', '.join(missing))
    compiler = result['compilerSha256']
    if compiler not in compilers:
        raise SourceUnitError('Unknown compiler identity: ' + str(compiler))
    result['compilerPath'] = compilers[compiler]
    processor = result['processor']
    if processor not in {'arm7', 'arm9'}:
        raise SourceUnitError('Unknown processor: ' + str(processor))
    if inventory['processor'] != processor:
        raise SourceUnitError('Processor disagrees with module inventory: ' + module)
    flags = validate_flags(result['compilerFlags'])
    base = result['loadAddressBase']
    if isinstance(base, int):
        base = hex(base)
    if not isinstance(base, str) or not re.fullmatch(r'0x[0-9a-fA-F]{1,8}', base):
        raise SourceUnitError('loadAddressBase must be a 32-bit hexadecimal address')
    image = canonical(result['originalImage'])
    if not image.startswith(ALLOWED_IMAGE_ROOTS):
        raise SourceUnitError('originalImage must name an extracted module image: ' + image)
    result.update(compilerFlags=flags, loadAddressBase=base, originalImage=image)
    return result


def load_config(root, data=None):
    if data is None:
        config_path = Path(root or '.') / CONFIG
        data = read_json(config_path)
    if not isinstance(data, dict):
        raise SourceUnitError('The source-unit configuration must be an object')
    extra = set(data) - {'schemaVersion', 'description', 'denominator', 'buildSha256', 'exclusions', 'compiler',
                         'compilers', 'modules', 'flagProfiles', 'generatedFrom', 'alternates', 'rules', 'objects'}
    if extra:
        raise SourceUnitError('Unsupported source-unit configuration fields: ' + ', '.join(sorted(extra)))
    if data.get('schemaVersion') != 1:
        raise SourceUnitError('Expected source-unit configuration schemaVersion 1')
    rules = data.get('rules')
    if not isinstance(rules, list):
        raise SourceUnitError('The source-unit configuration rules must be an array')
    modules = data.get('modules')
    if not isinstance(modules, dict) or not modules:
        raise SourceUnitError('The source-unit configuration has no module inventory')
    for name, entry in modules.items():
        if not isinstance(entry, dict) or set(entry) - {'processor', 'loadAddressBase', 'originalImage', 'bytes', 'program'}:
            raise SourceUnitError('Invalid module inventory entry: ' + str(name))
        if entry.get('processor') not in {'arm7', 'arm9'}:
            raise SourceUnitError('Unknown module processor: ' + str(name))
        if not isinstance(entry.get('loadAddressBase'), str):
            raise SourceUnitError('Module loadAddressBase is missing: ' + str(name))
    profiles = data.get('flagProfiles') or {}
    if not isinstance(profiles, dict):
        raise SourceUnitError('flagProfiles must be an object')
    for name, flags in profiles.items():
        validate_flags(flags, 'flagProfiles.' + str(name))
    compilers = data.get('compilers')
    if not isinstance(compilers, dict) or not compilers:
        raise SourceUnitError('The source-unit configuration has no compiler inventory')
    for identity, path in compilers.items():
        if not isinstance(identity, str) or not re.fullmatch(r'[0-9a-f]{64}', identity):
            raise SourceUnitError('Compiler inventory keys must be SHA-256 digests')
        if not isinstance(path, str) or not path.startswith('tools/'):
            raise SourceUnitError('Compiler inventory paths must stay under tools/')
    default_compiler = (data.get('compiler') or {}).get('sha256')
    if default_compiler not in compilers:
        raise SourceUnitError('The default compiler identity is missing from the compiler inventory')
    alternates = data.get('alternates') or {}
    if not isinstance(alternates, dict):
        raise SourceUnitError('alternates must be an object')
    for name, entries in alternates.items():
        canonical(name)
        if not isinstance(entries, list) or not entries:
            raise SourceUnitError('Alternate profiles must be a nonempty array: ' + name)
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) - {'compilerFlags', 'compilerSha256'}:
                raise SourceUnitError('Invalid alternate profile: ' + name)
            flags = entry.get('compilerFlags')
            if isinstance(flags, str):
                if flags not in profiles:
                    raise SourceUnitError('Unknown alternate compiler flag profile: ' + flags)
            else:
                validate_flags(flags, 'alternates.' + name)
            identity = entry.get('compilerSha256', default_compiler)
            if identity not in compilers:
                raise SourceUnitError('Unknown alternate compiler identity: ' + str(identity))
    fragments = read_rule_fragments(root) if root is not None else []
    ordered = [(origin, raw) for origin, entries in fragments for raw in entries]
    ordered.extend((CONFIG, raw) for raw in rules)
    if not ordered:
        raise SourceUnitError('The source-unit configuration has no rules')
    parsed = []
    scopes = {}
    origins = {}
    merge_order = []
    for origin, raw in ordered:
        try:
            rule = validate_rule(raw, modules)
        except SourceUnitError as error:
            raise SourceUnitError(str(error) + ' (in ' + origin + ')') from error
        if rule['scope'] in scopes:
            raise SourceUnitError("Duplicate source-unit rule glob '" + rule['scope'] + "' in "
                                  + origin + '; already declared in ' + origins[rule['scope']])
        scopes[rule['scope']] = rule
        origins[rule['scope']] = origin
        merge_order.append(rule['scope'])
        parsed.append(rule)
    parsed.sort(key=lambda item: depth(item['scope']))
    fragment_rule_count = len(ordered) - len(rules)
    objects = data.get('objects') or {}
    if not isinstance(objects, dict):
        raise SourceUnitError('objects must be an object keyed by source path')
    for source, entry in objects.items():
        canonical(source)
        if not isinstance(entry, dict) or set(entry) != {'object', 'sha256'}:
            raise SourceUnitError('An objects entry needs exactly object and sha256: ' + str(source))
        if not isinstance(entry['object'], str) or not entry['object']:
            raise SourceUnitError('An objects entry needs a nonempty object path: ' + str(source))
        if not isinstance(entry['sha256'], str) or not re.fullmatch(r'[0-9a-f]{64}', entry['sha256']):
            raise SourceUnitError('An objects entry needs a SHA-256 digest: ' + str(source))
        resolve(dict(rules=parsed, modules=modules, profiles=profiles, compilers=compilers,
                     default_compiler=default_compiler), source)
    exclusions = list(EXCLUSIONS) + list(data.get('exclusions') or [])
    for value in exclusions:
        scope_of(value)
    return dict(data=data, rules=parsed, scopes=scopes, origins=origins, mergeOrder=merge_order,
                modules=modules, profiles=profiles,
                compilers=compilers, default_compiler=default_compiler, alternates=alternates,
                exclusions=exclusions, objects=objects, fragments=[origin for origin, unused in fragments],
                fragmentRules=fragment_rule_count, baseRules=len(rules))


def matches(scope, name):
    return name == scope or name.startswith(scope + '/')


def resolve(config, name):
    name = canonical(name)
    chain = [rule['raw'] for rule in config['rules'] if matches(rule['scope'], name)]
    if not chain:
        raise SourceUnitError('No source-unit rule matches: ' + name)
    return merge_chain(chain, config['modules'], config['profiles'], config['compilers'],
                       config['default_compiler'])


def resolve_alternates(config, name):
    result = []
    for entry in config['alternates'].get(canonical(name), []):
        flags = entry.get('compilerFlags')
        if isinstance(flags, str):
            flags = config['profiles'][flags]
        identity = entry.get('compilerSha256', config['default_compiler'])
        result.append(dict(compilerFlags=list(flags), compilerSha256=identity,
                           compilerPath=config['compilers'][identity]))
    return result


def excluded(config, name):
    return any(matches(scope_of(pattern), name) for pattern in config['exclusions'])


def source_files(root):
    root = Path(root)
    result = []
    for path in (root / 'src').rglob('*'):
        if path.is_file():
            result.append(path.relative_to(root).as_posix())
    return sorted(result)


def enumerate_sources(root, config=None, check_all=False):
    config = config or load_config(root)
    files = source_files(root)
    compiled, excluded_files, unresolved, resolved = [], [], [], []
    assembly, prebuilt = [], []
    for name in files:
        if excluded(config, name):
            excluded_files.append(name)
            continue
        try:
            rule = resolve(config, name)
        except SourceUnitError as error:
            unresolved.append((name, str(error)))
            continue
        suffix = PurePosixPath(name).suffix.lower()
        if name.endswith('.c'):
            compiled.append(dict(path=name, alternates=resolve_alternates(config, name), **rule))
        elif suffix in {'.s', '.cpp'}:
            assembly.append(dict(path=name, kind=suffix[1:], alternates=resolve_alternates(config, name), **rule))
        entry = config['objects'].get(name)
        if entry is not None:
            prebuilt.append(dict(path=name, object=entry['object'], objectSha256=entry['sha256'], **rule))
        resolved.append((name, rule))
    if unresolved:
        detail = '; '.join(f'{name}: {reason}' for name, reason in unresolved[:20])
        raise SourceUnitError(f'{len(unresolved)} source file(s) match no unit rule: {detail}')
    return dict(config=config, files=files, compiled=compiled, excluded=excluded_files,
                assembly=assembly, prebuilt=prebuilt,
                resolved=resolved if check_all else None)


def check(root, config=None):
    config = config or load_config(root)
    result = enumerate_sources(root, config, check_all=True)
    by_module = {}
    by_extension = {}
    for name, rule in result['resolved']:
        by_module[rule['module']] = by_module.get(rule['module'], 0) + 1
        suffix = PurePosixPath(name).suffix or '<none>'
        by_extension[suffix] = by_extension.get(suffix, 0) + 1
    return dict(schemaVersion=1, configRules=len(config['rules']),
                baseRules=config['baseRules'], fragmentFiles=len(config['fragments']),
                fragmentRules=config['fragmentRules'],
                sourceFiles=len(result['files']),
                resolvedFiles=len(result['resolved']), excludedFiles=len(result['excluded']),
                compiledSources=len(result['compiled']), assemblySources=len(result['assembly']),
                prebuiltObjects=len(result['prebuilt']), modules=len(by_module),
                byModule=dict(sorted(by_module.items())), byExtension=dict(sorted(by_extension.items())),
                denominator=config['data'].get('denominator'), unresolved=0)


def main():
    parser = argparse.ArgumentParser(description='Resolve every public source file to one compilation rule.')
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--config', type=Path)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--rule', metavar='PATH')
    args = parser.parse_args()
    root = args.root.resolve()
    config_path = args.config or (root / CONFIG)
    try:
        config = load_config(root, read_json(config_path))
        if args.rule:
            print(json.dumps(resolve(config, args.rule), indent=2))
            return 0
        result = check(root, config)
        if args.list:
            for item in enumerate_sources(root, config)['compiled']:
                print('\t'.join((item['path'], item['module'], item['processor'],
                                 ','.join(item['compilerFlags']))))
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
