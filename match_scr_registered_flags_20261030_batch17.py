import hashlib
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261030/batch17'
WORK = ROOT / 'work/script-source/20261030/batch17/registered-flags'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-registered-flags.json'
PIN_PATHS = ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261030_v14.py',
    'nonmatching/script-source/20261029/native_scr_flags_20261029.py',
    'nonmatching/script-source/20261030/native_scr_registered_flags_20261030.py', 'evidence/encounter/script_assets_20261029.py',
    'evidence/encounter/vm_state_20261029.py', 'src/scripts/20261030/batch17/apply_registered_primary.c',
    'src/scripts/20261030/batch17/scr_registered_flags.h', 'src/scripts/20261030/batch17/registered.bindings.json')
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261030_v14.py': 'b0ee0e0fbc2b89d9e86be1a4928eab76c3da8838276c0a1b98f58e28ab310472',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_registered_flags_20261030.py': '2a58946fca687df319e3288ccc31b23a56f5b30dee12a48bdbef801f86ee02a5',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch17/apply_registered_primary.c': '084887ba1ffe0e821f3e3dccace1262fc5881a32113cbeff9b2be924af9f3f30',
 'src/scripts/20261030/batch17/scr_registered_flags.h': 'a84a47733ba2148fd1719589f1265ee535a6fca62ec836eb616497320c1615f6',
 'src/scripts/20261030/batch17/registered.bindings.json': '9061b4599bf0afb7c650a09b2c158aa87f18f2d58d432d5722991385149b0961'}
sys.path[:0] = [str(ROOT / 'evidence/encounter'), str(ROOT / 'nonmatching/script-source/20261029'),
    str(ROOT / 'nonmatching/script-source/20261030')]
import script_assets_20261029 as assets
import native_scr_registered_flags_20261030 as fixtures
import scr_c_compiler_20261030_v14 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def boundary(data):
    base, end = fixtures.BASE, fixtures.END
    assert [slot for slot, pc in data['entries'].items() if pc == base] == [259]
    assert not any(base < pc < end for pc in data['entries'].values())
    own = [row for row in data['instructions'] if base <= row['pc'] < end]
    assert sum(row['bytes'] for row in own) == 1128 and own[-1]['pc'] == end - 4 and own[-1]['opcode'] == 1026
    assert sum(row['opcode'] == 1026 for row in own) == 1
    incoming, locals_refs, globals_refs = [], [], []
    for row in data['instructions']:
        op, args = row['opcode'], row['argumentsRaw']
        if op in (1033, 1034, 1036, 1037, 1038) and base <= args[1] < end:
            incoming.append({'sourcePc': row['pc'], 'targetPc': args[1], 'opcode': op})
            assert not (base < args[1] < end and not base <= row['pc'] < end)
        pairs = []
        if op == 1045:
            pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read')]
        elif 1039 <= op <= 1044:
            pairs = [(args[1], args[2], 'read'), (args[3], args[4], 'read')]
        elif 1046 <= op <= 1053:
            pairs = [(args[i], args[i + 1], 'write' if i == 1 else 'read') for i in (1, 3, 5)]
        elif op == 1035:
            pairs = [(args[1], args[2], 'read')]
        for mode, raw, access in pairs:
            if mode != 0:
                continue
            slot = assets.f32(raw)
            assert slot == int(slot) and 0 <= slot < 256
            reference = {'pc': row['pc'], 'slot': int(slot), 'access': access}
            if int(slot) in (42, 43, 44):
                assert base <= row['pc'] < end
                locals_refs.append(reference)
            if 3 <= slot <= 22:
                globals_refs.append(reference)
    for slot in range(3, 23):
        rows = [row for row in globals_refs if row['slot'] == slot]
        assert sum(row['access'] == 'read' for row in rows) == 1 and sum(row['access'] == 'write' for row in rows) == 2
    return {'entry': 259, 'startPc': base, 'endExclusivePc': end, 'bytes': 1128, 'privateReturnPc': end - 4,
        'knownIncomingReferences': incoming, 'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
        'knownLocalSlotReferences': locals_refs, 'knownOutsideLocalSlotReferences': 0, 'knownModuleGlobalReferences': globals_refs,
        'moduleGlobalsAreNotPrivateLocals': True, 'moduleGlobalSlots': list(range(3, 23)), 'localSlots': [42, 43, 44],
        'moduleGlobalsNaturalInitializationAndRegistrationReachabilityProven': False,
        'allKnownMode0IndicesCanonical': True, 'reachableOwnRecordPcs': [row['pc'] for row in own],
        'serializedCompleteEntryDomainOnly': True, 'opaqueNativeOrComputedGlobalReferenceCoverageComplete': False}


def build(data):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(name, name) for name in PIN_PATHS[:2]] + [('src/scripts/20261030/batch17/' + name, name)
        for name in ('apply_registered_primary.c', 'scr_registered_flags.h', 'registered.bindings.json')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, 'scr_c_compiler_20261030_v14.py', '--source', 'apply_registered_primary.c', '--base', hex(fixtures.BASE),
        '--bindings', 'registered.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    assert body == data['code'][fixtures.BASE:fixtures.END] and len(body) == 1128
    rebuilt = bytearray(data['script'])
    rebuilt[4100 + fixtures.BASE:4100 + fixtures.END] = body
    assert bytes(rebuilt) == data['script']
    target = WORK / 'world.source-registered-flags.scr'
    target.write_bytes(rebuilt)
    return bytes(rebuilt), {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
        'inputs': [artifact(directory / name) for unused, name in files], 'emittedBody': artifact(directory / 'generated.scrfunc'),
        'compilerReport': artifact(directory / 'build.json'), 'compilerEvidence': json.loads((directory / 'build.json').read_text()),
        'rebuiltImage': artifact(target), 'originalBytecodeCompilerInput': False}


def controls(profile, data):
    directory = ROOT / 'nonmatching/script-source/20261030/batch17-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_registered_flags.h', directory / 'scr_registered_flags.h')
    text = (SOURCE / 'apply_registered_primary.c').read_text()
    tests = [('getter_negative', text.replace('get_primary_flag(flag_index)', 'get_primary_flag(-1)'), profile),
        ('getter1536', text.replace('get_primary_flag(flag_index)', 'get_primary_flag(1536)'), profile),
        ('setter1536', text.replace('set_primary_flag(flag_index, true)', 'set_primary_flag(1536, true)'), profile),
        ('uninitialized_boolean', text.replace('enabled = get_primary_flag(flag_index);', ''), profile),
        ('uninitialized_index', text.replace('float flag_index = -1;', 'float flag_index;'), profile),
        ('setter_value2', text.replace('set_primary_flag(flag_index, true)', 'set_primary_flag(flag_index, 2)'), profile),
        ('missing_module_object', text.replace('extern float registered_key_0;\n', ''), profile),
        ('no_final_return', text.replace('return candidate;', ''), profile),
        ('aliased_locals', text, {'locals': {'candidate': 42, 'flag_index': 42, 'enabled': 44}, 'globals': profile['globals']}),
        ('local_slot256', text, {'locals': {'candidate': 256, 'flag_index': 43, 'enabled': 44}, 'globals': profile['globals']})]
    rejected = []
    for name, source, bindings in tests:
        path = directory / (name + '.c')
        path.write_text(source)
        try:
            compiler.compile_source(path, fixtures.BASE, bindings)
        except ValueError as error:
            rejected.append({'name': name, 'source': artifact(path), 'bindings': bindings, 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Unsupported registered-flag source accepted: ' + name)
    excluded = []
    for name, raw in (('negative_index', fixtures.fword(-1)), ('index1536', fixtures.fword(1536)),
            ('fractional_index', fixtures.fword(31.5)), ('NaN_index', 0x7FC12345), ('infinite_index', 0x7F800000)):
        candidate = dict(fixtures.profiles()[0])
        candidate['indices'] = candidate['indices'].copy()
        candidate['indices'][0] = raw
        try:
            fixtures.execute(data['script'], candidate, 0, 2026103027999)
        except fixtures.UnsupportedPrimaryDomain as error:
            excluded.append({'name': name, 'profile': candidate, 'domainRejectedBeforeOwnEntryExecution': True,
                'nativeErrorPathClaimed': False, 'completeEntryReturnCredit': 0, 'postStopStateCredit': 0, 'reason': str(error)})
        else:
            raise AssertionError('Unsupported dynamic index context accepted')
    return {'rejectedSourceProfiles': rejected, 'unsupportedDynamicIndexContexts': excluded,
        'controlSourceCredit': 0, 'nativeErrorPathCredit': 0, 'generalModuleGlobalDomainProofClaimed': False}


def main():
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    for name, pin in PINS.items():
        assert digest((ROOT / name).read_bytes()) == pin, name
    data = assets.load(ROOT / 'extract/files/world.e')
    bounds = boundary(data)
    rebuilt, source_build = build(data)
    negative = controls(json.loads((SOURCE / 'registered.bindings.json').read_text()), data)
    print(json.dumps({'stage': 'source-only and domain controls passed', 'bytes': 1128}), flush=True)
    original = fixtures.run(data['script'])
    print(json.dumps({'stage': 'original complete', 'returns': original['actualReturningCalls']}), flush=True)
    recompiled = fixtures.run(rebuilt)
    assert original == recompiled and original['executedOwnRecordPcs'] == bounds['reachableOwnRecordPcs']
    unused, files = assets.original_files()
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'evidenceClass': 'ordinary-C-complete-registered-dynamic-primary-float-return-SCR-source-match', 'romSha256': assets.ROM_HASH,
        'sourceClosure': [{'path': name, 'sha256': pin} for name, pin in PINS.items()], 'asset': data['asset'],
        'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
        'romFileRange': list(files['world.e']), 'matchedRange': {'startPc': fixtures.BASE, 'endExclusivePc': fixtures.END,
        'bytes': 1128, 'sha256': digest(data['code'][fixtures.BASE:fixtures.END])}, 'boundariesAndStorage': bounds,
        'sourceOnlyBuild': source_build, 'compilerControls': negative, 'differential': original,
        'pairedCompleteOwnEntryExecutions': original['completeEntryExecutions'] * 2,
        'pairedNativeReturningCalls': original['actualReturningCalls'] * 2, 'sourceDefinitionCount': 1, 'completeFunctionInstances': 1,
        'qualifiedScriptRangeBytes': 1128, 'originalScaffoldingBytes': len(rebuilt) - 1128, 'scaffoldingSourceCredit': 0,
        'nativeExecutableByteCredit': 0, 'completeImagesRecovered': 0, 'nativeFunctionStubs': 0, 'postFaultStateUsedForProof': False,
        'wholeRomSourceMatch': False, 'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True,
        'limitations': ['Complete1128B entry259 only', 'Module-global keys/flag indices are explicit; natural producers/scene reachability unproved',
            'Only selected non-sentinel dynamic indices have qualified finite integral0..1535 domain',
            'Context-domain exclusions are not native rejection/error paths', 'Conditional set/reentry behavior does not prove once-ever or renewability',
            'No opaque/native/computed global control or complete image/ROM source claim']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'sourceBytes': 1128, 'completeEntries': report['pairedCompleteOwnEntryExecutions'],
        'nativeReturns': report['pairedNativeReturningCalls']}), flush=True)


if __name__ == '__main__':
    main()
