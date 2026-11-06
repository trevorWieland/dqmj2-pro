import copy
import gzip
import json
from pathlib import Path
import match_arm7_child_irq_dispatch260_20261101 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
MATCHER_SHA = 'ecef38cfdbad51dcb0e115d0dfc8ec5514d58009c1cfea6caad7eba6bf0e15c8'
_FRESH = None
CONTROL_REPORT = ROOT / 'evidence/verification' / ('arm7-' + Path(__file__).stem.removeprefix('validate_arm7_').removesuffix('_20261101').replace('_', '-') + '-controls-20261101.json')


def publish_controls(path, report):
    if path.resolve() != CONTROL_REPORT.resolve() or path.resolve() == REPORT.resolve():
        raise ValueError('Control publication escaped this validator namespace')
    write_json(path, report)


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Current host-alarm source/input/product changed: ' + str(name))
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name, MATCHER_SHA)
    pins = matcher.verify_inputs()
    matcher.qualified.inventory()
    names = {Path(matcher.__file__).name, matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins}
    if {row['path'] for row in report['generatorSources']} != names or len(report['generatorSources']) != len(names):
        raise ValueError('Complete host compiler/runtime/source closure differs')
    for row in report['generatorSources']:
        checked(row['path'], row['sha256'])
    if report['generatorSha256'] != MATCHER_SHA or report['generator'] != Path(matcher.__file__).name or report['pinnedGeneratorAndRuntimeDependencies'] != pins or report['romSha256'] != matcher.ROM:
        raise ValueError('Frozen host generator/input closure differs')
    expected = {'program': 'dwc/utility.bin/move/child.srl', 'processor': 'arm7', 'module': 'utility-child-arm7-wram',
        'matchedInitializedBytes': 260, 'matchedInstructionBytes': 212, 'generatedLiteralBytes': 48,
        'newOrdinaryFunctionCount': 8, 'newInitializedCoverageBytes': 260, 'declarationMigrationCount': 0,
        'declarationMigrationBytes': 0, 'ordinaryAssemblyOrBlobCredit': 0, 'originalDataSourceCredit': 0,
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Qualified host scope or source-only credit differs')
    rows, profile = report['matches'], json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 8 or len(profile) != 8:
        raise ValueError('Exactly eight complete child IRQ units required')
    for row, pin in zip(rows, profile):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Complete source/header/compiler/function identity differs')
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
    trace = report['sharedSourceLinkedNativeEvidence']['trace']
    compressed = checked(trace['path'], trace['compressedSha256']).read_bytes()
    if matcher.digest(gzip.decompress(compressed)) != trace['rawSha256'] or compressed[4:8] != bytes(4):
        raise ValueError('Complete deterministic native trace differs')
    if matcher.publication(rows) != (report['nativeSymbols'], report['nativeSymbolEntries']):
        raise ValueError('Qualified unchanged real-link bindings differ')
    if _FRESH is None:
        _FRESH = json.loads(json.dumps(matcher.proof()))
    current = {key: value for key, value in report.items() if key not in ('schemaVersion', 'generator', 'generatorSha256', 'generatorSources',
        'pinnedGeneratorAndRuntimeDependencies', 'romSha256', 'processor', 'program', 'module')}
    if current != _FRESH:
        raise ValueError('Fresh source-only linked host/native/model evidence differs')
    return {(row['processor'], row['program'], row['module'], row['address'], row['mode']): row for row in rows}


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
            raise ValueError('Invalid host source/evidence accepted: ' + name)

    changes=[('rom',('romSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),''),
        ('module',('module',),'arm7-wram'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),
        ('runtime',('pinnedGeneratorAndRuntimeDependencies',),[]),('coverage',('newInitializedCoverageBytes',),276),
        ('migration',('declarationMigrationCount',),1),('missing-entry',('matches',),[]),('mode',('matches',0,'mode'),'thumb'),
        ('source',('matches',0,'sourceSha256'),'0'*64),('header',('matches',7,'sourceDependencies'),[]),('flags',('matches',0,'compilerFlags'),[]),
        ('blob',('matches',0,'originalObjectScaffolding'),True),('exact-gate',('matches',7,'exactAfterDeclaredRelocation'),False),
        ('code-input',('matches',0,'sourceOnlyCompilerInput','originalCodeCompilerInput'),True),
        ('stub-invents-input',('matches',0,'sourceAbiContract','physicalArgumentWords'),1),
        ('dispatcher-loses-input',('matches',7,'sourceAbiContract','physicalArgumentWords'),0),
        ('record-width',('matches',7,'sourceAbiContract','callbackRecordBytes'),16),
        ('index-domain',('matches',7,'sourceAbiContract','definedDispatcherIndexDomain'),[0,9]),
        ('original-refusal',('matches',0,'originalDefaultLinkerRefusal'),'accepted'),
        ('scope-reference',('qualifiedCanonicalScope','sha256'),'0'*64),
        ('word-address',('fixedPlatformWord','address'),'0x0380fff4'),
        ('word-width',('matches',7,'fixedPlatformAbi','binding','width'),8),
        ('owned-return-inflation',('matches',0,'oracle','actualOriginalAndCompiledReturns'),50),
        ('tail-entries-as-returns',('sharedSourceLinkedNativeEvidence','sourceLinkedDispatcherTailEntriesSeparate'),999),
        ('callback-credit',('sharedSourceLinkedNativeEvidence','originalCallbackCodeOrDataCredit'),16),
        ('provider',('sharedSourceLinkedNativeEvidence','providerReplacements'),['BIOS']),
        ('budget-credit',('sharedSourceLinkedNativeEvidence','unsupportedReturnCredit'),1),
        ('data-credit',('originalDataSourceCredit',),18),('whole-module',('wholeModuleLinked',),True)]
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    reject('prior-batch-report-destination', lambda: publish_controls(ROOT / 'evidence/verification/arm7-host-irq244-controls-20261101.json', {}))
    for index, row in enumerate(report['matches']):
        for field, path in [('object', ROOT / row['object']), ('linked-body', Path(row['realArm7Link']['cwd']) / 'caller.bin')]:
            saved = path.read_bytes()
            try:
                path.unlink()
                reject('missing-' + str(index) + '-' + field, lambda: validate(report))
            finally:
                path.write_bytes(saved)
    path = ROOT / report['sharedSourceLinkedNativeEvidence']['trace']['path']
    saved = path.read_bytes()
    try:
        path.unlink()
        reject('missing-native-trace', lambda: validate(report))
    finally:
        path.write_bytes(saved)
    pins = json.loads(matcher.PROFILE.read_text())['matches']
    mutations=[('wrong-stub-index',0,'037fbb84(6)','037fbb84(5)',False),
        ('wrong-IRQ-combine',7,'NATIVE_IRQ_CHECK_WORD |= mask;','NATIVE_IRQ_CHECK_WORD &= mask;',False),
        ('callback-clear-erased',7,'[index].function = (void *)0;','[index].function = callback;',False),
        ('callback-argument-erased',7,'callback(native_utility_child_arm7_callbacks_0380594c[index].argument);','callback((void *)0);',False),
        ('enabled-width-truncated',7,'    u32 enabled;','    unsigned char enabled;',True),
        ('wrong-platform-word',7,'0x0380FFF8','0x0380FFF4',True)]
    mutations.append(('enabled-cached-before-callback',7,
        '    IrqCallback callback = native_utility_child_arm7_callbacks_0380594c[index].function;',
        '    u32 cachedEnabled = native_utility_child_arm7_callbacks_0380594c[index].enabled;\n    IrqCallback callback = native_utility_child_arm7_callbacks_0380594c[index].function;',False))
    for name, index, before, after, header_change in mutations:
        pin = pins[index]
        directory = matcher.WORK / 'controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        header = ROOT / pin['sourceDependencies'][0]['path']
        source = ROOT / pin['source']
        text = (header if header_change else source).read_text()
        if name=='enabled-cached-before-callback':
            text=text.replace('if (native_utility_child_arm7_callbacks_0380594c[index].enabled == 0)', 'if (cachedEnabled == 0)')
        if before not in text:
            raise ValueError('Expected ordinary-C mutation location absent')
        copied = directory / header.name
        copied.write_text(text.replace(before, after) if header_change else header.read_text())
        authored = directory / source.name
        authored.write_text(source.read_text() if header_change else text.replace(before, after))
        changed = dict(pin, source=authored.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(authored.read_bytes()),
            sourceDependencies=[{'path': copied.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(copied.read_bytes())}])
        reject('fresh-C-' + name, lambda changed=changed: matcher.build(changed))
    entry=report['matches'][0]
    dispatcher=report['matches'][7]
    for field,value in [('processor','arm9'),('program',''),('module','arm7-wram'),('mode','thumb'),
        ('address','0x37fbb04'),('bytes',12),('codeBytes',16),('targetSha256','0'*64),('inputModuleSha256','0'*64),
        ('qualifiedCanonicalScope',{})]:
        changed=dict(entry,**{field:value})
        reject('scope-caller-'+field,lambda changed=changed:matcher.qualified.guard(changed))
    for field,value in [('offset',8),('type',28),('explicitAddend',4),('symbol','native_utility_child_arm7_arm_037fbb88')]:
        changed=copy.deepcopy(entry)
        rel=next(item for item in changed['relocations']if item['symbol']=='native_utility_child_arm7_arm_037fbb84')
        rel[field]=value
        reject('stub-tail-relocation-'+field,lambda changed=changed:matcher.qualified.guard(changed))
    for field,value in [('address','0x37fbb80'),('bytes',144),('mode','thumb')]:
        changed=dict(dispatcher,**{field:value})
        reject('word-caller-'+field,lambda changed=changed:matcher.platform_abi.validate_binding(changed,matcher.platform_abi.BINDING))
    for field,value in [('address','0x0380fff4'),('width',8),('region','bss'),('dataSourceCredit',4)]:
        changed=dict(matcher.platform_abi.BINDING,**{field:value})
        reject('word-binding-'+field,lambda changed=changed:matcher.platform_abi.validate_binding(dispatcher,changed))
    modules,baseline=matcher.qualified.BASE_NAMESPACE(matcher.qualified.PROGRAM)
    for address in (0x0380FFF4,0x0380FFF8):
        reject('strict-data-'+hex(address),lambda address=address:matcher.linker.data_binding(entry,address,modules))
    before_host=matcher.qualified.BASE_NAMESPACE('')
    with matcher.qualified.installed(entry):
        actual=matcher.linker.namespace(matcher.qualified.PROGRAM)
        if set(actual[1])-set(baseline)!=set(matcher.qualified.SPECS) or matcher.linker.namespace('')!=before_host:
            raise ValueError('Scoped namespace added another entry or altered host namespace')
    if matcher.linker.namespace is not matcher.qualified.BASE_NAMESPACE:
        raise ValueError('Namespace not restored after successful context')
    controls.append({'name':'exact-eight-only-and-host-preserved','passed':True})
    path=ROOT/entry['object']
    saved=path.read_bytes()
    try:
        path.unlink()
        reject('failure-inside-installed-base-link',lambda:matcher.qualified.validate(entry,matcher.WORK/'controls'/'missing-installed-object'))
    finally:
        path.write_bytes(saved)
    if matcher.linker.namespace is not matcher.qualified.BASE_NAMESPACE:
        raise ValueError('Namespace not restored after actual base-link failure')
    controls.append({'name':'namespace-restored-after-error','passed':True})
    for pin in pins:
        matcher.build(pin)
    validate(report)
    path = CONTROL_REPORT
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()), 'controls': controls,
        'allPassed': all(row.get('rejected', row.get('passed',False)) for row in controls), 'newSourceBytes': 260, 'newFunctionCount': 8,
        'producerBeforeProductChecks': True, 'oldAcceptedSourcesAndHeaderUnchanged': True}
    publish_controls(path, result)
    print(json.dumps({'report': path.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(path.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
