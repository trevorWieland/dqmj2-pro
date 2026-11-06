import copy
import gzip
import json
from pathlib import Path
import match_arm7_child_alarm_handler256_20261101 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
CONTROL_REPORT = ROOT / 'evidence/verification' / ('arm7-' + Path(__file__).stem.removeprefix('validate_arm7_').removesuffix('_20261101').replace('_', '-') + '-controls-20261101.json')
MATCHER_SHA = '5127f8063bb21fe8061712da67653688cfed922443af782b12f59b5ece757329'
_FRESH = None


def publish(path, report):
    if path.resolve() != CONTROL_REPORT.resolve() or path.resolve() == REPORT.resolve():
        raise ValueError('Handler publication escaped own namespace')
    write_json(path, report)


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Current handler input/product missing or changed: ' + str(name))
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name, MATCHER_SHA)
    pins = matcher.verify_inputs()
    names = {Path(matcher.__file__).name, matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins}
    if {row['path'] for row in report['generatorSources']} != names or len(report['generatorSources']) != len(names):
        raise ValueError('Complete handler/dependency source closure differs')
    for row in report['generatorSources']:
        checked(row['path'], row['sha256'])
    if report['generatorSha256'] != MATCHER_SHA or report['generator'] != Path(matcher.__file__).name or report['pinnedGeneratorAndRuntimeDependencies'] != pins or report['romSha256'] != matcher.ROM:
        raise ValueError('Frozen source-only handler generator/runtime differs')
    expected = {'program': 'dwc/utility.bin/move/child.srl', 'processor': 'arm7', 'module': 'utility-child-arm7-wram', 'matchedInitializedBytes': 256,
        'matchedInstructionBytes': 244, 'generatedLiteralBytes': 12, 'newOrdinaryFunctionCount': 1,
        'newInitializedCoverageBytes': 256, 'sourceLinkedDependencyAdditionalCredit': 0, 'ordinaryAssemblyOrBlobCredit': 0,
        'originalDataSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
        'originalTickCallbackAndCallback16SourceCredit': 0, 'originalDataOrBssExtentCredit': 0,
        'fixedPlatformWord': matcher.platform_abi.BINDING}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Handler own scope or dependency credit differs')
    rows, profile = report['matches'], json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 1 or len(profile) != 1:
        raise ValueError('Exactly one complete handler required')
    for row, pin in zip(rows, profile):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen handler C/compiler/include identity differs')
    for row in rows:
        for name, field in [(row['source'], 'sourceSha256'), (row['compiler'], 'compilerSha256'), (row['object'], 'objectSha256')]:
            checked(name, row[field])
        for dependency in row['sourceDependencies']:
            checked(dependency['path'], dependency['sha256'])
        link = row['realArm7Link']
        checked(link['linkCommand'][0], link['linkerSha256'])
        checked(link['lcf'], link['lcfSha256'])
        checked(str(Path(link['cwd']) / 'caller.bin'), row['targetSha256'])
        checked(str(Path(link['cwd']) / 'linked.elf'), link['linkedElfSha256'])
        for anchor in link['zeroCodeAnchors']:
            checked(anchor['object'], anchor['objectSha256'])
    named = report['namedViewOriginalStrictRefusal']
    checked(named['object'], named['objectSha256'])
    trace = rows[0]['oracle']['trace']
    data = checked(trace['path'], trace['compressedSha256']).read_bytes()
    if matcher.digest(gzip.decompress(data)) != trace['rawSha256'] or data[4:8] != bytes(4):
        raise ValueError('Fresh raw/compressed native trace differs')
    if matcher.publication(rows) != (report['nativeSymbols'], report['nativeSymbolEntries']):
        raise ValueError('Qualified original real-link bindings differ')
    if _FRESH is None:
        _FRESH = json.loads(json.dumps(matcher.proof()))
    current = {key: value for key, value in report.items() if key not in ('schemaVersion', 'generator', 'generatorSha256', 'generatorSources',
        'pinnedGeneratorAndRuntimeDependencies', 'romSha256', 'processor', 'program', 'module')}
    if current != _FRESH:
        raise ValueError('Fresh handler/platform-word/full-memory effect proof differs')
    return {('arm7', 'dwc/utility.bin/move/child.srl', 'utility-child-arm7-wram', rows[0]['address'], 'arm'): rows[0]}


def main():
    matcher.main()
    report = json.loads(REPORT.read_text())
    validate(report)
    controls = []

    def reject(name, operation):
        try:
            operation()
        except Exception as error:
            controls.append({'name': name, 'rejected': True, 'exception': type(error).__name__, 'reason': str(error)})
        else:
            raise ValueError('Invalid handler source/evidence accepted: ' + name)

    changes = [('rom', ('romSha256',), '0' * 64), ('processor', ('processor',), 'arm9'), ('program', ('program',), 'utility'),
        ('module', ('module',), 'arm7-main'), ('generator', ('generatorSha256',), '0' * 64),
        ('closure', ('generatorSources',), []), ('runtime', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('dependency-credit', ('sourceLinkedDependencyAdditionalCredit',), 300), ('own-byte-inflation', ('newInitializedCoverageBytes',), 412),
        ('mode', ('matches', 0, 'mode'), 'thumb'), ('source', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('header', ('matches', 0, 'sourceDependencies'), []), ('flags', ('matches', 0, 'compilerFlags'), []),
        ('blob', ('matches', 0, 'originalObjectScaffolding'), True), ('exact-gate', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('code-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('named-view-refusal-lost', ('namedViewOriginalStrictRefusal', 'refusal'), 'accepted'),
        ('word-address', ('fixedPlatformWord', 'address'), '0x0380fff4'),
        ('word-width', ('fixedPlatformWord', 'width'), 8),
        ('word-data-credit', ('fixedPlatformWord', 'dataSourceCredit'), 4),
        ('platform-witness-returns', ('matches', 0, 'fixedPlatformAbi', 'witness', 'actualOriginalReturns'), 100),
        ('callback-credit', ('originalTickCallbackAndCallback16SourceCredit',), 136),
        ('return-inflation', ('matches', 0, 'oracle', 'actualOriginalAndCompiledReturns'), 170),
        ('unsupported-credit', ('matches', 0, 'oracle', 'unsupportedControls', 1, 'sourceReturnCredit'), 1),
        ('provider', ('matches', 0, 'oracle', 'providerReplacements'), ['timer']),
        ('budget-credit', ('matches', 0, 'oracle', 'unsupportedReturnCredit'), 1),
        ('data-credit', ('originalDataSourceCredit',), 44), ('whole-module', ('wholeModuleLinked',), True)]
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    row = report['matches'][0]
    named = report['namedViewOriginalStrictRefusal']
    products = [('missing-own-object', ROOT / row['object']),
        ('missing-named-refusal-object', ROOT / named['object']),
        ('missing-native-trace', ROOT / row['oracle']['trace']['path'])]
    for name, path in products:
        saved = path.read_bytes()
        try:
            path.unlink()
            reject(name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    for name, before, after in [('wrong-platform-mask', 'NATIVE_IRQ_CHECK_WORD |= 16;', 'NATIVE_IRQ_CHECK_WORD |= 8;'),
        ('wrong-time-predicate', 'now < entry->fire', 'now > entry->fire'),
        ('wrong-callback-argument', 'callback(entry->argument)', 'callback((void *)0)'),
        ('oneshot-retains-handler', 'entry->handler = (void *)0;', 'entry->handler = callback;')]:
        text = (ROOT / pin['source']).read_text()
        if before not in text:
            raise ValueError('Expected handler ordinary C expression absent')
        directory = matcher.WORK / 'controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        header = ROOT / pin['sourceDependencies'][0]['path']
        copied = directory / header.name
        copied.write_bytes(header.read_bytes())
        source = directory / Path(pin['source']).name
        source.write_text(text.replace(before, after))
        changed = dict(pin, source=source.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(source.read_bytes()),
            sourceDependencies=[{'path': copied.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(copied.read_bytes())}])
        reject('fresh-ordinary-C-' + name, lambda changed=changed: matcher.build(changed))
    reject('prior-callback76-publication', lambda: publish(ROOT / 'evidence/verification/arm7-child-timer-callback76-controls-20261101.json', {}))
    for field, value in [('processor', 'arm9'), ('program', ''), ('module', 'arm7-wram'), ('mode', 'thumb'),
        ('address', '0x37fd914'), ('bytes', 252), ('codeBytes', 240), ('inputModuleSha256', '0' * 64), ('targetSha256', '0' * 64)]:
        changed = dict(pin, **{field: value})
        reject('fixed-platform-caller-' + field, lambda changed=changed: matcher.platform_abi.validate_binding(changed, matcher.platform_abi.BINDING))
    for field, value in [('address', '0x0380fff4'), ('width', 8), ('region', 'bss'), ('dataSourceCredit', 4)]:
        changed = dict(matcher.platform_abi.BINDING, **{field: value})
        reject('fixed-platform-binding-' + field, lambda changed=changed: matcher.platform_abi.validate_binding(pin, changed))
    matcher.build(pin)
    validate(report)
    path = CONTROL_REPORT
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()), 'controls': controls,
        'allPassed': all(row['rejected'] for row in controls), 'newSourceBytes': 256, 'sourceLinkedDependencyAdditionalCredit': 0,
        'producerBeforeProductChecks': True, 'oldSourceAndHeaderUnchanged': True}
    publish(path, result)
    print(json.dumps({'report': path.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(path.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
