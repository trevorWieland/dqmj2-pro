import copy
import gzip
import json
from pathlib import Path
import match_arm7_alarm_oneshot112_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
MATCHER_SHA = 'b22c1b0c3442ef8b438bd98b38cd764efd7e3fc033879eb18e88b062c14f2f69'
_FRESH = None


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Current one-shot input/product missing or changed: ' + str(name))
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name, MATCHER_SHA)
    pins = matcher.verify_inputs()
    names = {Path(matcher.__file__).name, matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins}
    if {row['path'] for row in report['generatorSources']} != names or len(report['generatorSources']) != len(names):
        raise ValueError('Complete one-shot/dependency source closure differs')
    for row in report['generatorSources']:
        checked(row['path'], row['sha256'])
    if report['generatorSha256'] != MATCHER_SHA or report['generator'] != Path(matcher.__file__).name or report['pinnedGeneratorAndRuntimeDependencies'] != pins or report['romSha256'] != matcher.ROM:
        raise ValueError('Frozen source-only one-shot generator/runtime differs')
    expected = {'program': '', 'processor': 'arm7', 'module': 'arm7-wram', 'matchedInitializedBytes': 112,
        'matchedInstructionBytes': 112, 'generatedLiteralBytes': 0, 'newOrdinaryFunctionCount': 1,
        'newInitializedCoverageBytes': 112, 'sourceLinkedDependencyAdditionalCredit': 0, 'ordinaryAssemblyOrBlobCredit': 0,
        'originalDataSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('One-shot own scope or dependency credit differs')
    rows, profile = report['matches'], json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 1 or len(profile) != 1 or len(report['sourceLinkedDependencies']) != 1:
        raise ValueError('One own unit plus one zero-credit source-linked dependency required')
    for row, pin in zip(rows, profile):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen one-shot C/compiler/include identity differs')
    for row in rows + report['sourceLinkedDependencies']:
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
        raise ValueError('Fresh one-shot/source-linked dependency/full64-bit effect proof differs')
    return {('arm7', '', 'arm7-wram', rows[0]['address'], 'arm'): rows[0]}


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
            raise ValueError('Invalid one-shot source/evidence accepted: ' + name)

    changes = [('rom', ('romSha256',), '0' * 64), ('processor', ('processor',), 'arm9'), ('program', ('program',), 'utility'),
        ('module', ('module',), 'arm7-main'), ('generator', ('generatorSha256',), '0' * 64),
        ('closure', ('generatorSources',), []), ('runtime', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('dependency-credit', ('sourceLinkedDependencyAdditionalCredit',), 300), ('own-byte-inflation', ('newInitializedCoverageBytes',), 412),
        ('mode', ('matches', 0, 'mode'), 'thumb'), ('source', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('header', ('matches', 0, 'sourceDependencies'), []), ('flags', ('matches', 0, 'compilerFlags'), []),
        ('blob', ('matches', 0, 'originalObjectScaffolding'), True), ('exact-gate', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('code-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('dependency-missing', ('sourceLinkedDependencies',), []),
        ('dependency-code-credit', ('sourceLinkedDependencies', 0, 'ordinaryFunctionCredit'), 1),
        ('return-inflation', ('matches', 0, 'oracle', 'actualOriginalAndCompiledReturns'), 896),
        ('original-callee-as-source', ('matches', 0, 'oracle', 'sourceLinkedDependencyCount'), 0),
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
    products = [('missing-own-object', ROOT / row['object']),
        ('missing-dependency-body', Path(report['sourceLinkedDependencies'][0]['realArm7Link']['cwd']) / 'caller.bin'),
        ('missing-native-trace', ROOT / row['oracle']['trace']['path'])]
    for name, path in products:
        saved = path.read_bytes()
        try:
            path.unlink()
            reject(name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    for name, before, after in [('delay-truncated-to-word', 'entry, delay + now', 'entry, (u32)(delay + now)'),
        ('delay-subtracted', 'entry, delay + now', 'entry, delay - now')]:
        text = (ROOT / pin['source']).read_text()
        if before not in text:
            raise ValueError('Expected unsigned64 ordinary C expression absent')
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
    matcher.build(pin)
    validate(report)
    path = ROOT / 'evidence/verification/arm7-oneshot112-controls-20261031.json'
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()), 'controls': controls,
        'allPassed': all(row['rejected'] for row in controls), 'newSourceBytes': 112, 'sourceLinkedDependencyAdditionalCredit': 0,
        'producerBeforeProductChecks': True, 'oldSourceAndHeaderUnchanged': True}
    write_json(path, result)
    print(json.dumps({'report': path.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(path.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
