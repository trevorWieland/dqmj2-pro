import copy
import hashlib
import json
from pathlib import Path
import match_arm7_lane_channel_five_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'evidence/matches/arm7-lane-channel-five-20261031.json'
GENERATOR_SHA = '8052a1ffb6ae906ccbfecc90244b46452ff72c872dadb14c09825c994f01d1b5'
REFERENCE = {'kind': 'verified-public-sdk-reference-and-measured-native-channel-contracts', 'compilerInput': False}
_FRESH = {}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def path(name):
    result = (ROOT / name).resolve()
    if not result.is_relative_to(ROOT):
        raise ValueError('Channel-five input/product path escaped repository')
    return result


def verify_file(name, sha):
    current = path(name)
    if not current.is_file() or digest(current.read_bytes()) != sha:
        raise ValueError('Current channel-five input/product changed or missing: ' + name)
    return current


def derived_bindings(rows):
    symbols, entries = {}, []
    for row in rows:
        raw = verify_file(row['binary'], row['inputModuleSha256']).read_bytes()
        first = int(row['address'], 0) - row['base']
        for rel in row['relocations']:
            binding = row['realArm7Link']['bindings'][rel['symbol']]
            symbols[rel['symbol']] = binding['address']
            entries.append(dict(binding, symbol=rel['symbol'], sourceRelocationOffset=rel['offset'], sourceRelocationType=rel['type'],
                unchangedExplicitAddend=rel['explicitAddend'], nativeEncodedWord=hex(int.from_bytes(raw[first + rel['offset']:first + rel['offset'] + 4], 'little')), sourceCredit=0,
                callerIdentity={key: row[key] for key in ('program', 'processor', 'module', 'address', 'mode')}))
    return symbols, entries


def validate(report):
    if report.get('generator') != Path(matcher.__file__).name or report.get('generatorSha256') != GENERATOR_SHA:
        raise ValueError('Frozen channel-five matcher identity differs')
    verify_file(report['generator'], GENERATOR_SHA)
    verify_file(matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PROFILE_SHA)
    verify_file(matcher.PIN_FILE.relative_to(ROOT).as_posix(), matcher.PIN_SHA)
    pins = json.loads(matcher.PIN_FILE.read_text())['files']
    required = {report['generator'], matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PIN_FILE.relative_to(ROOT).as_posix()} | {item['path'] for item in pins}
    if len(report.get('generatorSources', [])) != len(required) or {row['path'] for row in report['generatorSources']} != required:
        raise ValueError('Complete channel-five generator closure differs')
    for item in report['generatorSources']:
        verify_file(item['path'], item['sha256'])
    pins = json.loads(matcher.PIN_FILE.read_text())['files']
    if report.get('pinnedGeneratorAndRuntimeDependencies') != pins:
        raise ValueError('Published frozen channel-five dependency closure differs')
    for item in pins:
        verify_file(item['path'], item['sha256'])
    verify_file('inputs/game.nds', matcher.ROM)
    if report.get('romSha256') != matcher.ROM or report.get('processor') != 'arm7' or report.get('program') != '' or report.get('module') != 'arm7-wram':
        raise ValueError('Channel-five qualified ROM/processor/module identity differs')
    if report.get('matchedInitializedBytes') != 780 or report.get('matchedInstructionBytes') != 688 or report.get('generatedLiteralBytes') != 92:
        raise ValueError('Measured channel-five code/literal coverage differs')
    if report.get('actualNativeAndCompiledReturns') != 11040 or report.get('actualSeparatelyObservedNestedReturns') != 4920 or report.get('providerFreeOriginalAndCompiledReturns') != 11040 or report.get('syntheticBiosContractOriginalAndCompiledReturns') != 0 or report.get('independentlyCheckedSigned64Returns') != 0 or report.get('originalBiosExecutionCredit') != 0:
        raise ValueError('Actual outer versus nested channel-five return counts differ')
    if report.get('wholeModuleLinked') is not False or report.get('sourceReconstructionComplete') is not False:
        raise ValueError('Channel-five scope overclaimed')
    if any(report.get(key) != 0 for key in ('ordinaryAssemblyOrBlobCredit', 'originalDataSourceCredit', 'calleeSourceCredit')):
        raise ValueError('Channel-five scaffold/original data/callee credit overstated')
    if report.get('referenceProvenance') != REFERENCE:
        raise ValueError('Reference-only typed source provenance differs')
    profile = json.loads(matcher.PROFILE.read_text())
    rows = report.get('matches', [])
    if len(rows) != 5:
        raise ValueError('Channel-five qualified source unit missing or duplicated')
    for pin, row in zip(profile['matches'], rows):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen typed channel-five source/profile differs')
        verify_file(pin['source'], pin['sourceSha256'])
        for item in pin['sourceDependencies']:
            verify_file(item['path'], item['sha256'])
        verify_file(pin['compiler'], pin['compilerSha256'])
        verify_file(row['object'], row['objectSha256'])
        proof = row['realArm7Link']
        verify_file(proof['linkCommand'][0], proof['linkerSha256'])
        verify_file(proof['lcf'], proof['lcfSha256'])
        verify_file(str(Path(proof['cwd']) / 'linked.elf'), proof['linkedElfSha256'])
        verify_file(str(Path(proof['cwd']) / 'caller.bin'), pin['targetSha256'])
        for anchor in proof['zeroCodeAnchors']:
            verify_file(anchor['object'], anchor['objectSha256'])
    symbols, entries = derived_bindings(rows)
    if report.get('nativeSymbols') != symbols or report.get('nativeSymbolEntries') != entries:
        raise ValueError('Published typed-channel-five function/data map differs from qualified real-link bindings/native addends')
    cache_key = digest(json.dumps(report['generatorSources'], sort_keys=True).encode())
    if cache_key not in _FRESH:
        _FRESH[cache_key] = dict(rows=json.loads(json.dumps([matcher.build(pin) for pin in profile['matches']])))
    if rows != _FRESH[cache_key]['rows']:
        raise ValueError('Published channel-five source/link/boundary/native records differ from full fresh proof')
    return {(row['processor'], row.get('program',''), row['module'], row['address'], row['mode']): row for row in rows}


def main():
    report = json.loads(REPORT.read_text())
    accepted = validate(report)
    controls = []
    def reject(name, operation):
        try:
            operation()
        except Exception as error:
            controls.append({'name': name, 'rejected': True, 'exception': type(error).__name__, 'reason': str(error)})
        else:
            raise ValueError('Invalid channel-five proof accepted: ' + name)
    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64),
        ('wrong-namespace', ('processor',), 'arm9'),
        ('whole-module-overclaim', ('wholeModuleLinked',), True),
        ('data-source-overclaim', ('originalDataSourceCredit',), 8),
        ('callee-source-overclaim', ('calleeSourceCredit',), 156),
        ('missing-generator-closure', ('generatorSources',), []),
        ('missing-runtime-closure', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('native-measurement-compiler-input', ('referenceProvenance', 'compilerInput'), True),
        ('inflated-entry-count', ('actualNativeAndCompiledReturns',), 1032),
        ('wrong-source-mode', ('matches', 0, 'mode'), 'thumb'),
        ('absent-link-comparison-flag', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('source-closure-mutation', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('original-code-compiler-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('false-return', ('matches', 0, 'oracle', 'verifiedReturn'), False),
        ('unsupported-return-credit', ('matches', 0, 'oracle', 'unsupportedReturnCredit'), 1),
        ('replaced-native-list-helpers', ('matches', 0, 'oracle', 'providerReplacements'), ['replacement']),
        ('invented-mute-r0-result', ('matches', 0, 'oracle', 'meaningfulReturnContract'), 'meaningful u32 result'),
        ('invented-result-contract', ('matches', 0, 'oracle', 'meaningfulReturnContract'), 'returns number of active records'),
        ('false-complete-game-state', ('matches', 0, 'oracle', 'limitations'), ['all save/game state initialized']),
        ('missing-native-symbol-map', ('nativeSymbols',), None),
        ('invented-native-symbol-entries', ('nativeSymbolEntries',), [{'mode': 'thumb'}]),
        ('invented-source-addend', ('matches', 0, 'realArm7Link', 'unchangedRelocations'), [{'explicitAddend': 4}]),
        ('invented-published-addend', ('nativeSymbolEntries',), [{'unchangedExplicitAddend': 4}]),
        ('invented-declared-include', ('matches', 0, 'sourceDependencies'), [{'path':'invented.h','sha256':'0'*64}]),
        ('physical-hardware-overclaim', ('matches', 0, 'oracle', 'hardwareExecutionCredit'), 1),
        ('unverified-full-state', ('matches', 0, 'oracle', 'fullRegistersFlagsStackAndMemoryCompared'), False),
        ('narrow-word-return-contract', ('matches', 0, 'oracle', 'meaningfulReturnContract'), 'u8 attenuation'),
        ('incomplete-own-coverage', ('matches', 0, 'oracle', 'allOwnInstructionAddressesVisited'), []),
    )
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        current = changed
        for key in keys[:-1]:
            current = current[key]
        current[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    first = report['matches'][0]
    binary = path(str(Path(first['realArm7Link']['cwd']) / 'caller.bin'))
    saved = binary.read_bytes()
    try:
        binary.unlink()
        reject('missing-current-linked-product-after-cache', lambda: validate(report))
        binary.write_bytes(bytes([saved[0] ^ 1]) + saved[1:])
        reject('changed-current-linked-product-after-cache', lambda: validate(report))
    finally:
        binary.write_bytes(saved)
    pins = json.loads(matcher.PROFILE.read_text())['matches']
    mutations = ((0,'wrong-pcm-source','reg_SOUNDoffSAD(off) = (u32)data;',
            'reg_SOUNDoffSAD(off) = (u32)data + 4u;'),
        (0,'wrong-timer-direction','(u16)(0x10000u - (u32)timer)','(u16)timer'),
        (1,'wrong-psg-control-bit','0x60000000','0x40000000'),
        (2,'wrong-requested-pan-cache','sOrgPan[chnIdx] = (u8)pan;','sOrgPan[chnIdx] = 0;'),
        (3,'wrong-scale-input','CalcSurroundDecay(vol, pan)','CalcSurroundDecay(volDiv, pan)'),
        (4,'wrong-volume-cache-source','CalcSurroundDecay(sOrgVolume[chnIdx], pan)',
            'CalcSurroundDecay(sOrgPan[chnIdx], pan)'))
    for index,name,old,new in mutations:
        pin=pins[index]
        original=path(pin['source']).read_text()
        changed_text=original.replace(old,new)
        if changed_text==original:
            raise ValueError('Expected channel-five source mutation absent')
        directory=matcher.WORK/'controls'/name
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/path(pin['source']).name
        source.write_text(changed_text)
        dependencies=[]
        for include in pin['sourceDependencies']:
            target=directory/path(include['path']).name
            target.write_bytes(path(include['path']).read_bytes())
            dependencies.append(dict(path=target.relative_to(ROOT).as_posix(),sha256=digest(target.read_bytes())))
        changed=dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=digest(source.read_bytes()),sourceDependencies=dependencies)
        reject('actual-compiler-link-rejects-'+name,lambda changed=changed:matcher.build(changed))
    native=matcher.fixture.fixture
    def require_return(value):
        if not value['states'][0]['actualReturn']:
            raise ValueError('Transfer bounded execution did not actually return')
    for pin in pins:
        address=int(pin['address'],0)
        raw=path(pin['binary']).read_bytes()
        body=raw[address-native.BASE:address-native.BASE+native.SIZES[address]]
        reject('channel-exhaustion-is-not-return-'+pin['address'],
            lambda address=address,body=body:require_return(native.execute(native.setup(address,body,native.cases(address)[0],91),budget=1)))
    for pin in pins:
        matcher.build(pin)
    identities={('arm7','','arm7-wram',pin['address'],'arm') for pin in pins}
    if set(validate(report))!=identities:
        raise ValueError('Qualified utility-child transfer identities differ')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': digest(REPORT.read_bytes()),
        'positiveUnits': len(accepted), 'matchedInitializedBytes': 780, 'actualOriginalAndCompiledReturns': 11040,
        'actualSeparateNestedReturns': 4920, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'negativeSourceVariants': 'Six independently compiled ordinary C register-data/timer/control/cache/scale mutations with complete copied header closure; accepted source remains unchanged'}
    destination = ROOT / 'evidence/verification/arm7-lane-channel-five-controls-20261031.json'
    write_json(destination, result)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
