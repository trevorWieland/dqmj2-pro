import hashlib
import json
import math
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261030/batch11'
WORK = ROOT / 'work/script-source/20261030/batch11/world17'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-world17.json'
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261029_v4.py': '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7',
 'scr_c_compiler_20261030_v6.py': 'ea44995cc5d9e13810a3d8f896b830a75b2cd42665a56b26d8289ef39df781a5',
 'scr_c_compiler_20261030_v9.py': '705c467d7edafcf9806b95f7736629895b5acc0b4b941aa462fc0a13b0bc53ba',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_world17_20261030.py': 'b792d912e9ceeb8c8a816d353d0af4c4d7d3f055168e1a99218d2b9d67bfd226',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch11/scr_random_decision.h': '5eb96e7af41e95c4b584894d20aaf1f813925c1c101e3c1f1813b341c27abe39',
 'src/scripts/20261030/batch11/selection.bindings.json': '03d60ee3490ba935d3c750a7821469b06915576a1d60e24b393aaeccc3d1309d',
 'src/scripts/20261030/batch11/select_numeric_thirty_one.c': '1a1ff545df5259a4ab11cb287840b3d10160c6e02e3afb18b9f4fc62f1cf9350'}
for path, sha in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261030'))
import script_assets_20261029 as assets
import native_scr_world17_20261030 as fixtures
import scr_c_compiler_20261030_v9 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def boundary(data, profile):
    start, end = fixtures.BASE, fixtures.END
    own = {r['pc']: r for r in data['instructions'] if start <= r['pc'] < end}
    assert [i for i, pc in data['entries'].items() if pc == start] == [17]
    assert not any(start < pc < end for pc in data['entries'].values())
    assert sum(r['bytes'] for r in own.values()) == 1148 and own[end - 4]['opcode'] == 1026
    assert sum(r['opcode'] == 1026 for r in own.values()) == 1
    by_slot = {value: key for key, value in profile['locals'].items()}
    refs, incoming = {name: [] for name in profile['locals']}, []
    for row in data['instructions']:
        op, x, pc = row['opcode'], row['argumentsRaw'], row['pc']
        if op in (1033, 1034, 1036, 1037, 1038) and start <= x[1] < end:
            incoming.append({'sourcePc': pc, 'targetPc': x[1], 'opcode': op})
            assert not (start < x[1] < end and pc not in own)
        pairs = [(x[1], x[2], 'write'), (x[3], x[4], 'read')] if op == 1045 else \
                [(x[1], x[2], 'read'), (x[3], x[4], 'read')] if 1039 <= op <= 1044 else \
                [(x[i], x[i + 1], 'write' if i == 1 else 'read') for i in (1, 3, 5)] if 1046 <= op <= 1053 else \
                [(x[1], x[2], 'read')] if op == 1035 else []
        for mode, raw, access in pairs:
            if mode != 0:
                continue
            value = struct.unpack('<f', struct.pack('<I', raw))[0]
            assert math.isfinite(value) and value == int(value) and 0 <= value < 256
            if int(value) in by_slot:
                assert pc in own
                refs[by_slot[int(value)]].append({'pc': pc, 'access': access})
    successors = {}
    for pc, row in own.items():
        op, x = row['opcode'], row['argumentsRaw']
        successors[pc] = [] if op == 1026 else [x[1]] if op == 1036 else [pc + row['bytes'], x[1]] if op == 1038 else [pc + row['bytes']]
        assert all(target in own for target in successors[pc])
    reached, todo = set(), [start]
    while todo:
        pc = todo.pop()
        if pc not in reached:
            reached.add(pc)
            todo += successors[pc]
    unreachable = sorted(set(own) - reached)
    assert unreachable == [59192, 59308, 59528]
    assert all(own[pc]['opcode'] == 1036 and own[pc - 12]['argumentsRaw'][1] == end - 4 for pc in unreachable)
    return {'entry': 17, 'startPc': start, 'endExclusivePc': end, 'bytes': 1148, 'privateReturnPc': end - 4,
        'knownIncomingReferences': incoming, 'knownSlotReferences': refs, 'knownOutsideSlotReferences': 0,
        'allKnownMode0IndicesCanonical': True, 'reachableOwnRecordPcs': sorted(reached),
        'compilerGeneratedUnreachableJoins': unreachable, 'unreachableJoinBytes': 36,
        'unreachableJoinsNotCountedAsExecuted': True, 'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
        'opaqueNativeOrComputedSlotReferenceCoverageComplete': False, 'serializedCompleteEntryDomainOnly': True}


def build(data):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(name, name) for name in ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py',
              'scr_c_compiler_20261030_v6.py', 'scr_c_compiler_20261030_v9.py')]
    files += [('src/scripts/20261030/batch11/' + name, name) for name in ('select_numeric_thirty_one.c', 'scr_random_decision.h', 'selection.bindings.json')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, 'scr_c_compiler_20261030_v9.py', '--source', 'select_numeric_thirty_one.c', '--base', hex(fixtures.BASE),
               '--bindings', 'selection.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    assert body == data['code'][fixtures.BASE:fixtures.END]
    rebuilt = data['script'][:4100 + fixtures.BASE] + body + data['script'][4100 + fixtures.END:]
    assert rebuilt == data['script']
    path = WORK / 'world.rebuilt.scr'
    path.write_bytes(rebuilt)
    return rebuilt, {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
        'inputs': [artifact(directory / target) for unused, target in files], 'emittedBody': artifact(directory / 'generated.scrfunc'),
        'compilerReport': artifact(directory / 'build.json'), 'compilerEvidence': json.loads((directory / 'build.json').read_text()),
        'rebuiltImage': artifact(path), 'originalBytecodeCompilerInput': False}


def byte_control(body, value):
    table = [-1] * 1024
    table[0] = 0
    script = b'SCR\0' + struct.pack('<1024i', *table) + body
    o = fixtures.Oracle(2026103019000 + value)
    state = o.persistent()
    state[fixtures.native.NUMERIC + 32 - fixtures.native.PERSIST] = value
    state[fixtures.native.NUMERIC + 30 - fixtures.native.PERSIST] = 0
    expected = bytearray(state)
    expected[fixtures.native.NUMERIC + 30 - fixtures.native.PERSIST] = 1 if value < 4 else 2 if value >= 8 else 0
    o.u.mem_write(fixtures.native.PERSIST, bytes(state))
    o.u.mem_write(fixtures.native.CODE - 4100, script)
    assert o.call(0x0204BC08, fixtures.native.CTX, fixtures.native.CODE - 4100) == 1
    assert o.call(0x0204BD00, fixtures.native.CTX, 0) == 1
    o.u.mem_write(fixtures.native.CTX + 3, b'\0')
    trace = []
    for unused in range(48):
        pc = o.read(fixtures.native.CTX + 0x470)
        op = struct.unpack_from('<I', body, pc)[0]
        assert o.call(0x0204C5A0 if op >= 1024 else 0x0205A65C, fixtures.native.CTX) == 1
        trace.append({'pc': pc, 'opcode': op, 'nextPc': o.read(fixtures.native.CTX + 0x470)})
        if not o.u.mem_read(fixtures.native.CTX + 0x476, 1)[0]:
            break
    else:
        raise ValueError('Synthetic byte-relation control failed to return')
    assert bytes(o.persistent()) == expected
    return {'numeric32': value, 'numeric30': 1 if value < 4 else 2 if value >= 8 else 0,
        'trace': trace, 'actualReturningCalls': o.returning_calls, 'observations': o.observations,
        'controlActuallyReturned': True, 'sourceCredit': 0}


def controls(profile):
    directory = ROOT / 'nonmatching/script-source/20261030/batch11-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_random_decision.h', directory / 'scr_random_decision.h')
    text = (SOURCE / 'select_numeric_thirty_one.c').read_text()
    tests = [('rng_zero', text.replace('sample_signed_random(6)', 'sample_signed_random(0)')),
        ('rng_overflow', text.replace('sample_signed_random(6)', 'sample_signed_random(257)')),
        ('rng_bool', text.replace('float selection', 'bool selection')),
        ('context_ordered', text.replace('get_numeric_state(32)', 'get_context_value(0)')),
        ('reversed_unqualified_operator', text.replace('state < 4', 'state > 4')),
        ('unqualified_left_variable_le', text.replace('8 <= state', 'state <= 8')),
        ('return_value', text.replace('return;', 'return 1;')),
        ('numeric_index', text.replace('get_numeric_state(32)', 'get_numeric_state(88)')),
        ('setter_value', text.replace('set_numeric_state(31, 59)', 'set_numeric_state(31, 256)')),
        ('changed_rng_provenance', text.replace('float selection = sample_signed_random(6);', 'float selection = get_context_value(0);\n    selection = sample_signed_random(6);'))]
    rejected = []
    for name, source in tests:
        path = directory / (name + '.c')
        path.write_text(source)
        try:
            compiler.compile_source(path, fixtures.BASE, profile)
        except ValueError as error:
            rejected.append({'name': name, 'source': artifact(path), 'bindings': profile, 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Unsupported random-decision source accepted: ' + name)
    path = directory / 'byte_relation_control.c'
    path.write_text('#include "scr_random_decision.h"\nvoid byte_relation_control(void)\n{\n    float value = get_numeric_state(32);\n    if (value < 4) { set_numeric_state(30, 1); }\n    if (8 <= value) { set_numeric_state(30, 2); }\n}\n')
    body, report = compiler.compile_source(path, 0, {'locals': {'value': 96}, 'globals': {}})
    assert len(body) == 280
    cases = [byte_control(body, value) for value in range(256)]
    return {'rejectedSourceProfiles': rejected, 'byteRelationSource': artifact(path), 'byteRelationBuild': report,
        'all256ByteRelationCases': cases, 'byteRelationActualReturningCalls': sum(c['actualReturningCalls'] for c in cases),
        'syntheticControlSourceCredit': 0, 'arbitraryContextFloatOrderingSupportClaimed': False}


def main():
    assert unicorn.__version__ == '2.1.4'
    for image, sha in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH), (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH),
                       (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == sha
    WORK.mkdir(parents=True, exist_ok=True)
    data = assets.load(ROOT / 'extract/files/world.e')
    assert data['scriptSha256'] == '9c6c4a136b306126a83a8a749df18276aa2a9d328a4add073fc47f50ea0619f8'
    profile = json.loads((SOURCE / 'selection.bindings.json').read_text())
    bounds = boundary(data, profile)
    rebuilt, source_build = build(data)
    negative = controls(profile)
    original, recompiled = fixtures.run(data['script']), fixtures.run(rebuilt)
    assert original == recompiled
    executed = {s['pc'] for c in original['cases'] for key in ('first', 'second') for s in c[key]['trace']}
    assert executed == set(bounds['reachableOwnRecordPcs'])
    rom, files = assets.original_files()
    report = {'schemaVersion': 1, 'generator': Path(__file__).relative_to(ROOT).as_posix(), 'generatorSha256': digest(Path(__file__).read_bytes()),
        'evidenceClass': 'ordinary-C-complete-bounded-random-early-return-SCR-source-match', 'romSha256': assets.ROM_HASH,
        'sourceClosure': [{'path': p, 'sha256': s} for p, s in PINS.items()], 'reproductionCommand': 'python match_scr_world17_20261030_batch11.py',
        'asset': data['asset'], 'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
        'romFileRange': list(files['world.e']), 'matchedRange': {'startPc': fixtures.BASE, 'endExclusivePc': fixtures.END, 'bytes': 1148,
        'sha256': digest(data['code'][fixtures.BASE:fixtures.END])}, 'boundariesAndStorage': bounds, 'sourceOnlyBuild': source_build,
        'compilerControls': negative, 'differential': original, 'executedOwnRecordPcs': sorted(executed),
        'allReachableOwnRecordsExecuted': True, 'unreachableCompilerJoinRecordsNotForced': True,
        'excludedBranchOutcomes': [{'pc': 60140, 'excludedValue': False, 'nativeBound': 6, 'selectionDomain': [0, 1, 2, 3, 4, 5],
            'earlierFalseEqualities': [0, 1, 2, 3, 4], 'remainingDomain': [5], 'outOfDomainRngInjected': False}],
        'sourceDefinitionCount': 1, 'completeFunctionInstances': 1, 'qualifiedScriptRangeBytes': 1148,
        'pairedNativeReturningCalls': original['actualReturningCalls'] * 2, 'pairedCompleteOwnEntryExecutions': original['freshMachines'] * 4,
        'syntheticByteControlNativeReturns': negative['byteRelationActualReturningCalls'], 'nativeExecutableByteCredit': 0,
        'originalScaffoldingBytes': len(rebuilt) - 1148, 'scaffoldingSourceCredit': 0, 'completeImagesRecovered': 0, 'nativeFunctionStubs': 0,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True, 'postFaultStateUsedForProof': False, 'wholeRomSourceMatch': False,
        'limitations': ['Complete1148B entry17 only; remaining original bytes/assets/native helpers carry no source credit',
            'Three compiler-generated unreachable joins are reproduced but never claimed executed',
            'Final selection==5 false outcome is excluded by genuine bound6 RNG and earlier0-4 exclusions',
            'Raw primary93/28,numeric31/32 values have no assigned area,timing,story,access or renewal meanings',
            'Known direct entries/encoded slot references are qualified; opaque/interior/native/global-program completeness is not claimed']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(OUTPUT), 'bytes': 1148, 'completeOwnEntryExecutions': report['pairedCompleteOwnEntryExecutions'],
        'nativeReturns': report['pairedNativeReturningCalls'], 'controlNativeReturns': report['syntheticByteControlNativeReturns']}))


if __name__ == '__main__':
    main()
