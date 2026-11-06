import copy
import gzip
import json
from pathlib import Path
import match_arm7_host_timer_init124_20261101 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
CONTROL_REPORT = ROOT / 'evidence/verification' / ('arm7-' + Path(__file__).stem.removeprefix('validate_arm7_').removesuffix('_20261101').replace('_', '-') + '-controls-20261101.json')
MATCHER_SHA = '7c3d2749580ebc8aab75f5b21e93db41af1c675cf3b43f3018ca1f21f6e796c2'
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
    expected = {'program': '', 'processor': 'arm7', 'module': 'arm7-wram', 'matchedInitializedBytes': 124,
        'matchedInstructionBytes': 112, 'generatedLiteralBytes': 12, 'newOrdinaryFunctionCount': 1,
        'newInitializedCoverageBytes': 124, 'sourceLinkedDependencyAdditionalCredit': 0, 'ordinaryAssemblyOrBlobCredit': 0,
        'originalDataSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
        'volatileTimerHardwareViews':{'0x04000100':2,'0x04000102':2}, 'counterAndResetViewBytes':{'counter':8,'reset':4},
        'ordinaryDataAbsoluteAddressGeneralizationAllowed':False,'newCanonicalScopeEntries':0,'qualifiedExtraCallbackPointerCount':1,'initializedDenominatorDelta':0,
        'oldUnacceptedObjectMetadataExcludedOnlyFromFrozenNativeProjection':True}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('One-shot own scope or dependency credit differs')
    rows, profile = report['matches'], json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 1 or len(profile) != 1 or len(report['sourceLinkedDependencies']) != 2:
        raise ValueError('One own unit plus one zero-credit source-linked dependency required')
    for row, pin in zip(rows, profile):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen one-shot C/compiler/include identity differs')
    if rows[0]['sourceAbiContract']['physicalArgumentWords']!=0 or rows[0]['sourceAbiContract']['return']!='void':
        raise ValueError('Initializer must preserve the actual void/zero-formal-argument API')
    if [row['ordinaryFunctionCredit']for row in report['sourceLinkedDependencies']]!=[0,0]:
        raise ValueError('Both complete callback/writer dependencies must have zero additional credit')
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
        ('return-inflation', ('matches', 0, 'oracle', 'actualOriginalAndCompiledReturns'), 578),
        ('counter-width',('counterAndResetViewBytes','counter'),4),
        ('reset-width',('counterAndResetViewBytes','reset'),1),
        ('timer-width',('volatileTimerHardwareViews','0x04000102'),4),
        ('writer-return-inflation',('matches',0,'oracle','actualFreshSourceLinkedWriterTailTransfersSeparate'),145),
        ('provider', ('matches', 0, 'oracle', 'providerReplacements'), ['timer']),
        ('budget-credit', ('matches', 0, 'oracle', 'unsupportedReturnCredit'), 1),
        ('data-credit', ('originalDataSourceCredit',), 44), ('whole-module', ('wholeModuleLinked',), True),
        ('denominator-inflation',('initializedDenominatorDelta',),104),
        ('invented-extra-entries',('newCanonicalScopeEntries',),2),
        ('tail-return-double-count',('matches',0,'oracle','tailTransfersAddNoSecondCallbackReturn'),False),
        ('installed-callback-return-inflation',('matches',0,'oracle','actualFreshSourceLinkedInstalledCallbackReturnsSeparate'),1152),
        ('historical-metadata-projection-claim',('oldUnacceptedObjectMetadataExcludedOnlyFromFrozenNativeProjection',),False),
        ('extra-callback-pointer-inflation',('qualifiedExtraCallbackPointerCount',),2),
        ('own-physical-argument-fabrication',('matches',0,'sourceAbiContract','physicalArgumentWords'),1),
        ('writer-code-credit',('sourceLinkedDependencies',1,'ordinaryFunctionCredit'),1)]
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    row = report['matches'][0]
    products = [('missing-own-object', ROOT / row['object']),
        ('missing-callback-body', Path(report['sourceLinkedDependencies'][0]['realArm7Link']['cwd']) / 'caller.bin'),
        ('missing-writer-body',Path(report['sourceLinkedDependencies'][1]['realArm7Link']['cwd'])/'caller.bin'),
        ('missing-native-trace', ROOT / row['oracle']['trace']['path'])]
    for name, path in products:
        saved = path.read_bytes()
        try:
            path.unlink()
            reject(name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    for name,before,after in [('initialized-branch-reversed',
        'native_host_arm7_timer_state_03807898.initialized == 0','native_host_arm7_timer_state_03807898.initialized != 0'),
        ('counter-initializes-one','native_host_arm7_timer_state_03807898.counter = 0;','native_host_arm7_timer_state_03807898.counter = 1;'),
        ('reset-not-cleared','native_host_arm7_timer_state_03807898.reset = 0;','native_host_arm7_timer_state_03807898.reset = 1;'),
        ('wrong-irq-mask','037fb7bc(8,','037fb7bc(16,')]:
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
    reject('prior-host104-publication', lambda: publish(ROOT / 'evidence/verification/arm7-host-tick-callback104-controls-20261101.json', {}))
    qualified=row
    for name,keys,value in [('scope-wrong-program',('program',),'utility'),('scope-wrong-mode',('mode',),'thumb'),
        ('scope-wrong-entry',('address',),'0x37fd12c'),('scope-wrong-size',('bytes',),120),
        ('scope-code-as-pool',('codeBytes',),108),('scope-wrong-module',('module',),'arm7-main'),
        ('scope-wrong-build',('inputModuleSha256',),'0'*64),('scope-wrong-target',('targetSha256',),'0'*64),
        ('scope-reference',('qualifiedCanonicalScope',),{}),('scope-mutated-addend',('relocations',0,'explicitAddend'),4)]:
        changed=copy.deepcopy(qualified)
        target=changed
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value
        reject(name,lambda changed=changed:matcher.scoped.guard(changed))
    before=matcher.scoped.BASE_NAMESPACE
    reject('unchanged-default-linker-refusal',lambda:matcher.linker.validate(qualified,matcher.WORK/'controls/default-refusal'))
    reject('default-unknown-data-preserved',lambda:matcher.linker.data_binding(qualified,0x0380FFF8,before('')[0]))
    if controls[-1].get('exception')!='ValueError' or controls[-1].get('reason')!='Unqualified external ARM7 data target: 0x380fff8':
        raise ValueError('Default data negative did not reach the unchanged meaningful guard')
    path=ROOT/qualified['object'];saved=path.read_bytes()
    try:
        path.unlink()
        reject('actual-link-failure-inside-installed-adapter',lambda:matcher.scoped.validate(qualified,matcher.WORK/'controls/missing-object-link'))
    finally:path.write_bytes(saved)
    if matcher.linker.namespace is not before:
        raise ValueError('Namespace not restored after actual installed-link failure')
    controls.append({'name':'namespace-restored-after-real-failure','rejected':True,'reason':'Original namespace function identity restored in finally'})
    child_before=before('dwc/utility.bin/move/child.srl')
    with matcher.scoped.installed(qualified):
        if matcher.linker.namespace('dwc/utility.bin/move/child.srl')!=child_before:
            raise ValueError('Host adapter altered child namespace')
    if matcher.linker.namespace is not before:
        raise ValueError('Namespace not restored after success')
    controls.append({'name':'child-namespace-preserved-and-success-restored','rejected':True,'reason':'Other program namespace unchanged; original function restored'})
    reject('partial-execution-body',lambda:matcher.fixture.engine.setup({0x037FD1B4:b'1234'},0))
    scope_report=matcher.scoped.callback.witness.REPORT
    saved=scope_report.read_bytes()
    try:
        scope_report.unlink()
        reject('missing-current-original-boundary-witness',lambda:matcher.scoped.guard(qualified))
    finally:scope_report.write_bytes(saved)
    matcher.build(pin)
    validate(report)
    path = CONTROL_REPORT
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()), 'controls': controls,
        'allPassed': all(row['rejected'] for row in controls), 'newSourceBytes': 124, 'sourceLinkedDependencyAdditionalCredit': 0,
        'producerBeforeProductChecks': True, 'oldSourceAndHeaderUnchanged': True}
    publish(path, result)
    print(json.dumps({'report': path.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(path.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
