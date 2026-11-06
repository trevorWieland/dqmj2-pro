import copy
import gzip
import json
from pathlib import Path
import match_arm7_child_alarm_programmer156_20261031 as matcher
from project import ROOT, write_json

MATCHER_SHA = '5019b71c2a56eafe376bf4637b21362c6d3374752c22e564e11f43f2c7b01963'
_FRESH = None
CONTROL_REPORT = ROOT / 'evidence/verification' / ('arm7-' + Path(__file__).stem.removeprefix('validate_arm7_').removesuffix('_20261031').replace('_', '-') + '-controls-20261031.json')


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Current qualified programmer source/input/product changed: ' + str(name))
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name, MATCHER_SHA)
    pins = matcher.verify_inputs()
    names = {Path(matcher.__file__).name, matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins}
    if len(report['generatorSources']) != len(names) or {row['path'] for row in report['generatorSources']} != names:
        raise ValueError('Complete programmer/source-getter/boundary closure differs')
    for row in report['generatorSources']:
        checked(row['path'], row['sha256'])
    if report['generatorSha256'] != MATCHER_SHA or report['generator'] != Path(matcher.__file__).name or report['pinnedGeneratorAndRuntimeDependencies'] != pins or report['romSha256'] != matcher.ROM:
        raise ValueError('Pinned qualified programmer generator/build/runtime differs')
    expected = {'program': matcher.qualified.PROGRAM, 'processor': 'arm7', 'module': matcher.qualified.MODULE,
        'matchedInitializedBytes': 156, 'matchedInstructionBytes': 140, 'generatedLiteralBytes': 16,
        'newOrdinaryFunctionCount': 1, 'newInitializedCoverageBytes': 156, 'sourceLinkedDependencyAdditionalCredit': 0,
        'callbackSourceCredit': 0, 'callbackQualifiedBoundaryBytes': 16, 'additionalInitializedDenominatorBytes': 0,
        'ordinaryAssemblyOrBlobCredit': 0, 'originalDataSourceCredit': 0, 'wholeModuleLinked': False,
        'sourceReconstructionComplete': False, 'qualifiedBoundaryReference': matcher.qualified.REFERENCE}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Qualified source extent/identity or callback/dependency credit differs')
    rows, profile = report['matches'], json.loads(matcher.PROFILE.read_text())
    if len(rows) != 1 or len(report['sourceLinkedDependencies']) != 1:
        raise ValueError('One complete programmer plus one zero-credit C dependency required')
    for row, pin in [(rows[0], profile['matches'][0]), (report['sourceLinkedDependencies'][0], profile['sourceLinkedDependency'])]:
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen programmer or source-getter C/compiler/include identity differs')
        for name, field in [(row['source'], 'sourceSha256'), (row['object'], 'objectSha256'), (row['compiler'], 'compilerSha256')]:
            checked(name, row[field])
        for header in row['sourceDependencies']:
            checked(header['path'], header['sha256'])
        link = row['realArm7Link']
        checked(link['linkCommand'][0], link['linkerSha256'])
        checked(link['lcf'], link['lcfSha256'])
        checked(str(Path(link['cwd']) / 'caller.bin'), row['targetSha256'])
        checked(str(Path(link['cwd']) / 'linked.elf'), link['linkedElfSha256'])
        for anchor in link['zeroCodeAnchors']:
            checked(anchor['object'], anchor['objectSha256'])
    matcher.qualified.guard(rows[0])
    if matcher.publication(rows) != (report['nativeSymbols'], report['nativeSymbolEntries']):
        raise ValueError('Qualified original callback/callee/MMIO bindings differ')
    trace = rows[0]['oracle']['trace']
    data = checked(trace['path'], trace['compressedSha256']).read_bytes()
    if matcher.digest(gzip.decompress(data)) != trace['rawSha256'] or data[4:8] != bytes(4):
        raise ValueError('Fresh full native/model source-linked trace differs')
    if _FRESH is None:
        _FRESH = json.loads(json.dumps(matcher.proof()))
    current = {key: value for key, value in report.items() if key not in ('schemaVersion', 'generator', 'generatorSha256', 'generatorSources',
        'pinnedGeneratorAndRuntimeDependencies', 'romSha256', 'processor', 'program', 'module')}
    if current != _FRESH:
        raise ValueError('Fresh full C/real-link/narrow-boundary/native-memory proof differs')
    return {(row['processor'], row['program'], row['module'], row['address'], row['mode']): row for row in rows}


def publish(path, report):
    if path.resolve() != CONTROL_REPORT.resolve() or path.resolve() == matcher.REPORT.resolve():
        raise ValueError('Programmer control publication escaped its own namespace')
    write_json(path, report)


def main():
    matcher.main()
    report = json.loads(matcher.REPORT.read_text())
    validate(report)
    controls = []

    def reject(name, operation):
        try:
            operation()
        except Exception as failure:
            controls.append({'name': name, 'rejected': True, 'exception': type(failure).__name__, 'reason': str(failure)})
        else:
            raise ValueError('Invalid programmer scope/source/evidence accepted: ' + name)

    changes = [('rom', ('romSha256',), '0' * 64), ('closure', ('generatorSources',), []), ('runtime', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('callback-source-credit', ('callbackSourceCredit',), 16), ('denominator-double-add', ('additionalInitializedDenominatorBytes',), 16),
        ('dependency-credit', ('sourceLinkedDependencyAdditionalCredit',), 176), ('scope-reference', ('qualifiedBoundaryReference',), {}),
        ('own-byte-inflation', ('newInitializedCoverageBytes',), 172), ('mode', ('matches', 0, 'mode'), 'thumb'),
        ('source', ('matches', 0, 'sourceSha256'), '0' * 64), ('header', ('matches', 0, 'sourceDependencies'), []),
        ('blob', ('matches', 0, 'originalObjectScaffolding'), True), ('exact-gate', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('return-inflation', ('matches', 0, 'oracle', 'actualOriginalAndCompiledReturns'), 192),
        ('callback-execution-claim', ('matches', 0, 'oracle', 'callbackInvokedByThisProof'), True),
        ('source-dependency-missing', ('sourceLinkedDependencies',), []),
        ('dependency-function-credit', ('sourceLinkedDependencies', 0, 'ordinaryFunctionCredit'), 1),
        ('whole-module', ('wholeModuleLinked',), True)]
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    original = report['matches'][0]
    guard_changes = [('processor', 'arm9'), ('program', ''), ('module', 'arm7-wram'), ('mode', 'thumb'),
        ('address', hex(matcher.qualified.CALLER + 4)), ('bytes', 152), ('codeBytes', 136),
        ('targetSha256', '0' * 64), ('inputModuleSha256', '0' * 64), ('qualifiedCanonicalScope', {})]
    for key, value in guard_changes:
        reject('caller-guard-' + key, lambda key=key, value=value: matcher.qualified.guard(dict(original, **{key: value})))
    for key, value in [('processor', 'arm9'), ('program', ''), ('module', 'arm7-wram'), ('mode', 'thumb'),
        ('address', '0x37fd8fc'), ('address', '0x37fd904'), ('address', '0x37fd910'), ('bytes', 12), ('codeSha256', '0' * 64)]:
        entry = copy.deepcopy(original)
        entry['qualifiedCanonicalScope'][key] = value
        reject('callback-guard-' + key + '-' + str(value), lambda entry=entry: matcher.qualified.guard(entry))
    for key, value in [('offset', 0x94), ('type', 1), ('explicitAddend', 1), ('symbol', 'native_utility_child_arm7_arm_037fd904')]:
        entry = copy.deepcopy(original)
        relocation = next(row for row in entry['relocations'] if row['symbol'] == 'native_utility_child_arm7_arm_037fd900')
        relocation[key] = value
        reject('unchanged-pointer-relocation-' + key, lambda entry=entry: matcher.qualified.guard(entry))
    for name, path in [('own-object', ROOT / original['object']),
        ('getter-body', Path(report['sourceLinkedDependencies'][0]['realArm7Link']['cwd']) / 'caller.bin'),
        ('native-trace', ROOT / original['oracle']['trace']['path'])]:
        saved = path.read_bytes()
        try:
            path.unlink()
            reject('missing-' + name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    with matcher.qualified.installed(original):
        base = matcher.qualified.BASE_NAMESPACE(matcher.qualified.PROGRAM)[1]
        extended = matcher.linker.namespace(matcher.qualified.PROGRAM)[1]
        if set(extended) - set(base) != {matcher.qualified.CALLBACK} or any(extended[key] != value for key, value in base.items()):
            raise ValueError('Namespace extended more than the single measured callback')
        if matcher.linker.namespace('')[1] != matcher.qualified.BASE_NAMESPACE('')[1]:
            raise ValueError('Child callback qualification affected host namespace')
    if matcher.linker.namespace is not matcher.qualified.BASE_NAMESPACE:
        raise ValueError('Original namespace not restored after successful scope context')
    controls.append({'name': 'single-child-entry-only-and-success-restoration', 'passed': True, 'kind': 'positive', 'reason': 'Only 037FD900 added; other namespaces unchanged; original restored'})
    broken = dict(original, object=(matcher.WORK / 'missing-new-object.o').relative_to(ROOT).as_posix())
    reject('base-validation-error-inside-scope', lambda: matcher.qualified.validate(broken, matcher.WORK / 'controls/failed-base-link'))
    if matcher.linker.namespace is not matcher.qualified.BASE_NAMESPACE:
        raise ValueError('Original namespace not restored after base linker exception')
    controls.append({'name': 'exception-restoration', 'passed': True, 'kind': 'positive', 'reason': 'Original namespace restored in finally'})
    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    for name, before, after in [('wrong-negative-count', 'count = 0xFFFE;', 'count = 0xFFFF;'),
        ('wrong-sign-branch', 'if (delta < 0)', 'if (delta > 0)'),
        ('wrong-callback-argument', '037fd900, NULL)', '037fd900, entry)')]:
        directory = matcher.WORK / 'controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        header = ROOT / pin['sourceDependencies'][0]['path']
        copied = directory / header.name
        copied.write_bytes(header.read_bytes())
        source = directory / Path(pin['source']).name
        text = (ROOT / pin['source']).read_text()
        if before not in text:
            raise ValueError('Ordinary C mutation location absent')
        source.write_text(text.replace(before, after))
        changed = dict(pin, source=source.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(source.read_bytes()),
            sourceDependencies=[{'path': copied.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(copied.read_bytes())}])
        reject('fresh-C-' + name, lambda changed=changed: matcher.build(changed))
    matcher.build(pin)
    validate(report)
    reject('prior-tick324-publication', lambda: publish(ROOT / 'evidence/verification/arm7-child-tick324-controls-20261031.json', {}))
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': matcher.REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(matcher.REPORT.read_bytes()),
        'controls': controls, 'allPassed': all(row.get('rejected', row.get('passed', False)) for row in controls),
        'negativeControls': sum(row.get('rejected', False) for row in controls), 'positiveRestorationControls': sum(row.get('kind') == 'positive' for row in controls), 'newSourceBytes': 156,
        'callbackSourceCredit': 0, 'getterAdditionalCredit': 0, 'additionalInitializedDenominatorBytes': 0,
        'originalNamespaceRestored': matcher.linker.namespace is matcher.qualified.BASE_NAMESPACE}
    publish(CONTROL_REPORT, result)
    print(json.dumps({'report': CONTROL_REPORT.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(CONTROL_REPORT.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
