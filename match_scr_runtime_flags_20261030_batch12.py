import hashlib
import json
import math
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261030/batch12'
WORK = ROOT / 'work/script-source/20261030/batch12/runtime-flags'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-runtime-flags.json'
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261030_v10.py': '80257ee6d3a118f3897ad406fde8983cc317e132cf7bd357761c44ff76253a08',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_runtime_flags_20261030.py': 'bbef9876e1dfd1c3d367fb685ee957831de2b3e8d92a88080dfbb8627410f202',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch12/clear_primary_range_450_498.c': '9e7677d28489afd7fc5b8deabfcf369d02af45b3be85a16d5a44eca9604a562a',
 'src/scripts/20261030/batch12/range.locals.json': '644c8c99da056bdebb20217dafb0b0c5610d3890ecada6ba310afe949d5b8d07',
 'src/scripts/20261030/batch12/scr_runtime_flags.h': 'b946aa46b02ff0df705daaaee84a65f9ab8ffe267371050f33e312aafceb8575'}
for path, pin in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == pin, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261030'))
import script_assets_20261029 as assets
import native_scr_runtime_flags_20261030 as fixtures
import scr_c_compiler_20261030_v10 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def boundary(data):
    start, end = fixtures.BASE, fixtures.END
    own = {row['pc']: row for row in data['instructions'] if start <= row['pc'] < end}
    assert [i for i, pc in data['entries'].items() if pc == start] == [257]
    assert not any(start < pc < end for pc in data['entries'].values())
    assert sum(row['bytes'] for row in own.values()) == 220 and own[end - 4]['opcode'] == 1026
    incoming, refs = [], []
    for row in data['instructions']:
        op, args, pc = row['opcode'], row['argumentsRaw'], row['pc']
        if op in (1033, 1034, 1036, 1037, 1038) and start <= args[1] < end:
            incoming.append({'sourcePc': pc, 'targetPc': args[1], 'opcode': op})
            assert not (start < args[1] < end and pc not in own)
        pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read')] if op == 1045 else \
                [(args[1], args[2], 'read'), (args[3], args[4], 'read')] if 1039 <= op <= 1044 else \
                [(args[i], args[i + 1], 'write' if i == 1 else 'read') for i in (1, 3, 5)] if 1046 <= op <= 1053 else \
                [(args[1], args[2], 'read')] if op == 1035 else []
        for mode, raw, access in pairs:
            if mode == 0:
                slot = struct.unpack('<f', struct.pack('<I', raw))[0]
                assert math.isfinite(slot) and slot == int(slot) and 0 <= slot < 256
                if slot == 33:
                    assert pc in own
                    refs.append({'pc': pc, 'access': access})
    successors = {}
    for pc, row in own.items():
        op, x = row['opcode'], row['argumentsRaw']
        successors[pc] = [] if op == 1026 else [x[1]] if op == 1036 else [pc + row['bytes'], x[1]] if op == 1038 else [pc + row['bytes']]
        assert all(target in own for target in successors[pc])
    reachable, pending = set(), [start]
    while pending:
        pc = pending.pop()
        if pc not in reachable:
            reachable.add(pc)
            pending += successors[pc]
    assert set(own) - reachable == {1248}
    return {'entry': 257, 'startPc': start, 'endExclusivePc': end, 'bytes': 220, 'privateReturnPc': end - 4,
        'knownIncomingReferences': incoming, 'knownCounterReferences': refs, 'knownOutsideCounterReferences': 0,
        'allKnownMode0IndicesCanonical': True, 'reachableOwnRecordPcs': sorted(reachable),
        'compilerGeneratedUnreachableJoins': [1248], 'unreachableJoinBytes': 12,
        'unreachableJoinNotCountedAsExecuted': True, 'externalInteriorEntries': 0,
        'opaqueNativeOrComputedSlotReferenceCoverageComplete': False, 'serializedCompleteEntryDomainOnly': True}


def build(data):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(n, n) for n in ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261030_v10.py')]
    files += [('src/scripts/20261030/batch12/' + n, n) for n in ('clear_primary_range_450_498.c', 'scr_runtime_flags.h', 'range.locals.json')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, 'scr_c_compiler_20261030_v10.py', '--source', 'clear_primary_range_450_498.c', '--base', hex(fixtures.BASE),
               '--locals', 'range.locals.json', '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    assert body == data['code'][fixtures.BASE:fixtures.END]
    rebuilt = data['script'][:4100 + fixtures.BASE] + body + data['script'][4100 + fixtures.END:]
    assert rebuilt == data['script']
    path = WORK / 'world.rebuilt.scr'
    path.write_bytes(rebuilt)
    return rebuilt, {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
        'inputs': [artifact(directory / name) for unused, name in files], 'emittedBody': artifact(directory / 'generated.scrfunc'),
        'compilerReport': artifact(directory / 'build.json'), 'compilerEvidence': json.loads((directory / 'build.json').read_text()),
        'rebuiltImage': artifact(path), 'originalBytecodeCompilerInput': False}


def controls():
    directory = ROOT / 'nonmatching/script-source/20261030/batch12-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_runtime_flags.h', directory / 'scr_runtime_flags.h')
    text = (SOURCE / 'clear_primary_range_450_498.c').read_text()
    cases = [('negative_start', text.replace('int flag = 450', 'int flag = -1')), ('empty', text.replace('flag < 499', 'flag < 450')),
        ('reverse', text.replace('flag < 499', 'flag < 449')), ('out_of_bounds', text.replace('flag < 499', 'flag < 1537')),
        ('wrong_condition', text.replace('flag < 499', 'flag <= 499')), ('wrong_counter_use', text.replace('set_primary_flag(flag', 'set_primary_flag(450')),
        ('nonboolean', text.replace('false', '2')), ('increment_mismatch', text.replace('++flag', '++other')),
        ('extra_body', text.replace('set_primary_flag(flag, false);', 'set_primary_flag(flag, false); set_primary_flag(flag, true);'))]
    rejected = []
    for label, source in cases:
        path = directory / (label + '.c')
        path.write_text(source)
        try:
            compiler.compile_source(path, fixtures.BASE, {'flag': 33})
        except ValueError as error:
            rejected.append({'name': label, 'source': artifact(path), 'allocation': {'flag': 33}, 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Invalid runtime-loop source accepted: ' + label)
    synthetic = []
    for start, limit, enabled in ((0, 1, False), (31, 33, True), (1535, 1536, False)):
        path = directory / ('boundary_' + str(start) + '.c')
        path.write_text('#include "scr_runtime_flags.h"\nvoid boundary_control(void)\n{\n    for (int flag = ' + str(start) + '; flag < ' + str(limit) + '; ++flag) { set_primary_flag(flag, ' + ('true' if enabled else 'false') + '); }\n}\n')
        body, compiled = compiler.compile_source(path, 0, {'flag': 33})
        table = [-1] * 1024
        table[0] = 0
        script = b'SCR\0' + struct.pack('<1024i', *table) + body
        o = fixtures.Oracle(2026103020000 + start)
        initial = bytes(o.persistent())
        o.u.mem_write(fixtures.native.CODE - 4100, script)
        assert o.call(0x0204BC08, fixtures.native.CTX, fixtures.native.CODE - 4100) == 1
        assert o.call(0x0204BD00, fixtures.native.CTX, 0) == 1
        o.u.mem_write(fixtures.native.CTX + 3, b'\0')
        result = fixtures.invocation(o, script, 0, start, limit, enabled, 0, len(body), 33)
        synthetic.append({'source': artifact(path), 'compilerEvidence': compiled, 'start': start, 'limit': limit,
            'enabled': enabled, 'initialPersistentHex': initial.hex(), 'result': result, 'observations': o.observations,
            'actualReturningCalls': o.returning_calls, 'sourceCredit': 0})
    return {'rejectedSourceProfiles': rejected, 'boundaryControls': synthetic, 'controlSourceCredit': 0,
        'boundaryControlActualReturningCalls': sum(c['actualReturningCalls'] for c in synthetic)}


def main():
    assert unicorn.__version__ == '2.1.4'
    for image, pin in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH), (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH),
                       (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == pin
    WORK.mkdir(parents=True, exist_ok=True)
    data = assets.load(ROOT / 'extract/files/world.e')
    assert data['scriptSha256'] == '9c6c4a136b306126a83a8a749df18276aa2a9d328a4add073fc47f50ea0619f8'
    bounds = boundary(data)
    rebuilt, source_build = build(data)
    negative = controls()
    original, recompiled = fixtures.run(data['script']), fixtures.run(rebuilt)
    assert original == recompiled
    executed = {step['pc'] for case in original['cases'] for key in ('first', 'second') for step in case[key]['trace']}
    assert executed == set(bounds['reachableOwnRecordPcs'])
    rom, files = assets.original_files()
    report = {'schemaVersion': 1, 'generator': Path(__file__).relative_to(ROOT).as_posix(), 'generatorSha256': digest(Path(__file__).read_bytes()),
        'evidenceClass': 'ordinary-C-complete-runtime-primary-flag-loop-SCR-source-match', 'romSha256': assets.ROM_HASH,
        'sourceClosure': [{'path': p, 'sha256': s} for p, s in PINS.items()], 'reproductionCommand': 'python match_scr_runtime_flags_20261030_batch12.py',
        'asset': data['asset'], 'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
        'romFileRange': list(files['world.e']), 'matchedRange': {'startPc': fixtures.BASE, 'endExclusivePc': fixtures.END, 'bytes': 220,
        'sha256': digest(data['code'][fixtures.BASE:fixtures.END])}, 'boundariesAndStorage': bounds,
        'sourceOnlyBuild': source_build, 'compilerControls': negative, 'differential': original,
        'executedOwnRecordPcs': sorted(executed), 'allReachableOwnRecordsExecuted': True, 'unreachableCompilerJoinNotForced': True,
        'sourceDefinitionCount': 1, 'completeFunctionInstances': 1, 'qualifiedScriptRangeBytes': 220,
        'pairedCompleteOwnEntryExecutions': original['freshMachines'] * 4, 'pairedNativeReturningCalls': original['actualReturningCalls'] * 2,
        'pairedPrimarySetterExecutions': original['freshMachines'] * 4 * 49,
        'separateBoundaryControlNativeReturns': negative['boundaryControlActualReturningCalls'],
        'originalScaffoldingBytes': len(rebuilt) - 220, 'scaffoldingSourceCredit': 0, 'nativeExecutableByteCredit': 0,
        'completeImagesRecovered': 0, 'nativeFunctionStubs': 0, 'postFaultStateUsedForProof': False, 'wholeRomSourceMatch': False,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True,
        'limitations': ['Complete220B entry257 only; remaining code/assets/native helpers carry no reconstructed-source credit',
            'Runtime C counter integers450-499 are exactly represented by the VM binary32 storage; general integer arithmetic is not claimed',
            'Original compiler join1248 is unreachable from the qualified entry and is not forced for coverage',
            'Known direct entries and encoded slot33 references are qualified; opaque/native/global-program coverage remains incomplete',
            'Repeated clearing of raw flags450-498 has no assigned story,area,access or encounter-renewal meaning']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(OUTPUT), 'bytes': 220, 'completeOwnEntryExecutions': report['pairedCompleteOwnEntryExecutions'],
        'nativeReturns': report['pairedNativeReturningCalls'], 'setterExecutions': report['pairedPrimarySetterExecutions'],
        'controlNativeReturns': report['separateBoundaryControlNativeReturns']}))


if __name__ == '__main__':
    main()
