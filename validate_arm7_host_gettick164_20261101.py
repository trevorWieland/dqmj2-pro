import copy
import gzip
import json
from pathlib import Path
import match_arm7_host_gettick164_20261101 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
CONTROL_REPORT = ROOT / 'evidence/verification' / ('arm7-' + Path(__file__).stem.removeprefix('validate_arm7_').removesuffix('_20261101').replace('_', '-') + '-controls-20261101.json')
MATCHER_SHA = 'c0bcb1656dfbeb906ad936d91a3f8a009bd77e72df2d4a5c12fdc4380d5a1745'
_FRESH = None


def publish(path, report):
    if path.resolve() != CONTROL_REPORT.resolve() or path.resolve() == REPORT.resolve():
        raise ValueError('Callback writer publication escaped own namespace')
    write_json(path, report)


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
    expected = {'program': '', 'processor': 'arm7', 'module': 'arm7-wram', 'matchedInitializedBytes': 164,
        'matchedInstructionBytes': 152, 'generatedLiteralBytes': 12, 'newOrdinaryFunctionCount': 1,
        'newInitializedCoverageBytes': 164, 'sourceLinkedDependencyAdditionalCredit': 0, 'ordinaryAssemblyOrBlobCredit': 0,
        'originalDataSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
        'volatileTimerHardwareViews':{'0x04000100':2,'0x04000214':4},'counterViewBytes':8,'counterMaskBits':48,
        'compatibleTickStateViewBytes':16,'sharedCounterAccessQualificationIsNewHypothesis':True,
        'counterGlobalDeclarationChanged':False,'counterMmioOrHistoricalQualifierClaimed':False,
        'ordinaryDataAbsoluteAddressGeneralizationAllowed':False}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('One-shot own scope or dependency credit differs')
    rows, profile = report['matches'], json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 1 or len(profile) != 1 or len(report['sourceLinkedDependencies']) != 3:
        raise ValueError('One own unit plus one zero-credit source-linked dependency required')
    for row, pin in zip(rows, profile):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen one-shot C/compiler/include identity differs')
    if rows[0]['sourceAbiContract']['physicalArgumentWords']!=0 or rows[0]['sourceAbiContract']['return']!='u64-r0-r1':
        raise ValueError('Getter must preserve the actual zero-formal unsigned64 ABI')
    if [row['ordinaryFunctionCredit']for row in report['sourceLinkedDependencies']]!=[0,0,0]:
        raise ValueError('All three freshly compiled producer units have zero additional coverage')
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
        ('return-inflation', ('matches', 0, 'oracle', 'actualOriginalAndCompiledReturns'), 770),
        ('counter-width',('counterViewBytes',),4),('counter-mask',('counterMaskBits',),64),
        ('sample-width',('volatileTimerHardwareViews','0x04000100'),4),
        ('pending-width',('volatileTimerHardwareViews','0x04000214'),2),
        ('source-arity-fabrication',('matches',0,'sourceAbiContract','physicalArgumentWords'),1),
        ('source-return-truncation',('matches',0,'sourceAbiContract','return'),'u32'),
        ('old-volatile-provenance-invented',('counterMmioOrHistoricalQualifierClaimed',),True),
        ('global-type-migration-invented',('counterGlobalDeclarationChanged',),True),
        ('qualification-claim-erased',('sharedCounterAccessQualificationIsNewHypothesis',),False),
        ('read-order-erased',('matches',0,'oracle','exactTimerCounterCounterLowHighPendingObservationOrder'),False),
        ('initializer-credit',('sourceLinkedDependencies',0,'ordinaryFunctionCredit'),1),
        ('callback-credit',('sourceLinkedDependencies',1,'ordinaryFunctionCredit'),1),
        ('writer-credit',('sourceLinkedDependencies',2,'ordinaryFunctionCredit'),1),
        ('producer-return-inflation',('matches',0,'oracle','actualFreshSourceLinkedProducerReturnsSeparate','initialize'),384),
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
        ('missing-initializer-body',Path(report['sourceLinkedDependencies'][0]['realArm7Link']['cwd'])/'caller.bin'),
        ('missing-callback-body',Path(report['sourceLinkedDependencies'][1]['realArm7Link']['cwd'])/'caller.bin'),
        ('missing-writer-body',Path(report['sourceLinkedDependencies'][2]['realArm7Link']['cwd'])/'caller.bin'),
        ('missing-native-trace', ROOT / row['oracle']['trace']['path'])]
    for name, path in products:
        saved = path.read_bytes()
        try:
            path.unlink()
            reject(name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    for name,before,after in [('unqualified-counter-observation',
        '*(volatile u64 *)&native_host_arm7_timer_state_03807898.counter','native_host_arm7_timer_state_03807898.counter'),
        ('counter-truncated-mask','0xFFFFFFFFFFFFULL','0xFFFFFFFFULL'),
        ('wrong-pending-bit','NATIVE_IRQ_REQUEST & 8','NATIVE_IRQ_REQUEST & 4'),
        ('reverse-half-range','!(sample & 0x8000)','(sample & 0x8000)'),
        ('wrong-irq-restoration','037fdd14(irq)','037fdd14(0)')]:
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
    reject('prior-init124-publication', lambda: publish(ROOT / 'evidence/verification/arm7-host-timer-init124-controls-20261101.json', {}))
    reject('partial-source-chain-execution',lambda:matcher.fixture.engine.setup({0x037FD21C:b'1234'},0))
    matcher.build(pin)
    validate(report)
    path = CONTROL_REPORT
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()), 'controls': controls,
        'allPassed': all(row['rejected'] for row in controls), 'newSourceBytes': 164, 'sourceLinkedDependencyAdditionalCredit': 0,
        'producerBeforeProductChecks': True, 'oldSourceAndHeaderUnchanged': True}
    publish(path, result)
    print(json.dumps({'report': path.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(path.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
