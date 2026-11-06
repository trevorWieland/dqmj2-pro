import ast
import hashlib
import importlib.util
import json
import random
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHARED = ROOT / 'validate_scr_numeric_transition_20261029_batch04.py'
if hashlib.sha256(SHARED.read_bytes()).hexdigest() != 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020':
    raise ValueError('Frozen validation helper')
spec = importlib.util.spec_from_file_location('_runtime_flags_shared', SHARED)
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_runtime_flags_20261030_batch12.py'
MATCHER_HASH = '4aa270e05a37ae5028642a9ecb6a4d99d431d81cd3614ec270f8f8373e7a8576'
REPORT = 'evidence/matches/scripts-20261030-runtime-flags.json'
BASE, END = 1056, 1276
PERSIST, PRIMARY = 0x021B9EB4, 0x021C0E20


def word(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def expected_trace(base, start, limit):
    offsets, opcodes = [0, 12, 36], [1036, 1045, 1024]
    for index in range(start, limit):
        offsets += [44, 56, 80, 104, 112, 144, 168]
        opcodes += [1036, 1045, 1045, 42, 1046, 1044, 1038]
        offsets += [180] if index + 1 == limit else [204]
        opcodes += [1036]
    offsets += [216]
    opcodes += [1026]
    return [{'pc': base + offset, 'opcode': opcode, 'nextPc': base + (offsets[i + 1] if i + 1 < len(offsets) else offset)}
            for i, (offset, opcode) in enumerate(zip(offsets, opcodes))]


def invocation(part, before, registers, observations, start=450, limit=499, enabled=False, base=BASE):
    trace = expected_trace(base, start, limit)
    require(part['trace'] == trace and part['completeEntryReturned'] is True, 'Exact complete runtime-loop trace/private return')
    require(part['registerFileBeforeHex'] == bytes(registers).hex(), 'Complete counter register-file carry')
    require(len(observations) == len(trace), 'Actual returning-call population for runtime loop')
    state, counter, setters, stores = bytearray(before), start, [], []
    for step, observation in zip(trace, observations):
        offset, op = step['pc'] - base, step['opcode']
        if offset == 12:
            struct.pack_into('<I', registers, 33 * 4, word(start))
        elif op == 42:
            previous = int(bool(state[PRIMARY + counter // 8 - PERSIST] & (1 << (counter & 7))))
            byte, mask = PRIMARY + counter // 8 - PERSIST, 1 << (counter & 7)
            state[byte] = state[byte] | mask if enabled else state[byte] & ~mask
            setters.append({'index': counter, 'enabled': enabled, 'previous': previous})
            address = PRIMARY + (counter >> 5) * 4
            stores.append({'address': hex(address), 'bytes': 4, 'value': struct.unpack_from('<I', state, address - PERSIST)[0]})
        elif op == 1046:
            counter += 1
            struct.pack_into('<I', registers, 33 * 4, word(counter))
        require(observation['entry'] == ('0x205a65c' if op < 1024 else '0x204c5a0') and observation['resultWord'] == 1
                and observation['persistentSha256'] == digest(state), 'Native result/full persistent effect per iteration step')
    require(counter == limit and part['iterations'] == limit - start and part['setters'] == setters
            and part['counterValuesAfterIncrements'] == list(range(start + 1, limit + 1)), 'Every runtime counter and primary index')
    require(part['branchOutcomes'] == [False] * (limit - start - 1) + [True], 'Every loop continuation and sole exit')
    require(part['orderedPrimaryWordStores'] == stores and part['persistentBeforeSha256'] == digest(before)
            and part['persistentAfterSha256'] == digest(state), 'Ordered aligned-word RMW and neighboring bytes')
    require(part['registerFileAfterSha256'] == digest(registers) and part['finalCounterWord'] == word(limit)
            and part['allOtherSlotsPreserved'] is True and part['neighboringPrimaryBitsPreserved'] is True,
            'Exact floating representation of finite C integer counter and all other slots')
    return bytes(state)


def native_proof(report):
    proof = report['differential']
    require(len(proof['cases']) == proof['freshMachines'] == 16 and proof['nativeInstructionCap'] == 20000
            and proof['nativeTimeoutMicroseconds'] == 1000000 and proof['scriptStepCap'] == 816
            and proof['runtimeIterationsPerInvocation'] == 49 and proof['serializedCompleteCallsOnly'] is True
            and proof['directEntryDomainOnly'] is True and proof['naturalSceneOrRenewabilityMeaningProven'] is False, 'Execution bounds/scope')
    calls, executed = 0, set()
    for index, case in enumerate(proof['cases']):
        pattern, thread = ('zero', 'ones', 'alternating', 'random')[index // 4], index % 4
        seed = 2026103018000 + index
        require(case['pattern'] == pattern and case['thread'] == thread and case['seed'] == seed, 'Fresh machine/bit-pattern/thread population')
        state = bytearray(random.Random(seed).randbytes(0x7040))
        offset = PRIMARY - PERSIST
        if pattern in ('zero', 'ones'):
            state[offset:offset + 192] = bytes([0 if pattern == 'zero' else 255]) * 192
        elif pattern == 'alternating':
            state[offset:offset + 192] = bytes([0xAA, 0x55]) * 96
        registers = bytearray(random.Random(seed ^ 0xC12).randbytes(1024))
        observed = case['observations']
        shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([item['entry'] for item in observed[:len(startup)]] == startup
                and all(item['persistentSha256'] == digest(state) for item in observed[:len(startup)]), 'Native init/start/forks')
        cursor = len(startup)
        for ordinal, key in enumerate(('first', 'second')):
            if ordinal:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0')
                        and observed[cursor]['persistentSha256'] == digest(state), 'Natural serialized loop reentry')
                cursor += 1
            part = case[key]
            end = cursor + len(part['trace'])
            state = invocation(part, state, registers, observed[cursor:end])
            executed.update(row['pc'] for row in part['trace'])
            cursor = end
        require(case['second']['persistentBeforeSha256'] == case['second']['persistentAfterSha256'], 'Reentry repeats setters without renewed persistent changes')
        require(cursor == len(observed) == case['actualReturningCalls'], 'Native return totals')
        calls += cursor
    require(executed == set(report['boundariesAndStorage']['reachableOwnRecordPcs']) and report['executedOwnRecordPcs'] == sorted(executed)
            and report['allReachableOwnRecordsExecuted'] is True and report['unreachableCompilerJoinNotForced'] is True, 'Only reachable records count as executed')
    require(calls == proof['actualReturningCalls'] == 12744 and report['pairedNativeReturningCalls'] == calls * 2
            and report['pairedCompleteOwnEntryExecutions'] == 64 and report['pairedPrimarySetterExecutions'] == 64 * 49,
            'Separate complete-entry/native helper/setter counts')


def controls(matcher, report):
    controls = report['compilerControls']
    require(len(controls['rejectedSourceProfiles']) == 9 and controls['controlSourceCredit'] == 0, 'Source/domain rejection population')
    for item in controls['rejectedSourceProfiles']:
        source = checked(ROOT, item['source'])
        require((source.parent / 'scr_runtime_flags.h').read_bytes() == (matcher.SOURCE / 'scr_runtime_flags.h').read_bytes(), 'Control include identity')
        try:
            matcher.compiler.compile_source(source, BASE, item['allocation'])
        except ValueError as error:
            require(str(error) == item['error'] and item['rejectedBeforeOutput'] is True, 'Reproducible source/domain error')
        else:
            raise ValueError('Unsupported runtime loop source compiles')
    require(len(controls['boundaryControls']) == 3, 'Actual boundary and word-crossing controls')
    calls = 0
    for case, (start, limit, enabled) in zip(controls['boundaryControls'], ((0, 1, False), (31, 33, True), (1535, 1536, False))):
        require((case['start'], case['limit'], case['enabled'], case['sourceCredit']) == (start, limit, enabled, 0), 'Synthetic boundary identity')
        source = checked(ROOT, case['source'])
        body, compiled = matcher.compiler.compile_source(source, 0, {'flag': 33})
        require(len(body) == 220 and json.loads(json.dumps(compiled)) == case['compilerEvidence'], 'Fresh boundary C compilation')
        observed = case['observations']
        shared.observations(observed)
        initial = random.Random(2026103020000 + start).randbytes(0x7040)
        require(case['initialPersistentHex'] == initial.hex() and observed[0]['persistentSha256'] == digest(initial)
                and [item['entry'] for item in observed[:2]] == ['0x204bc08', '0x204bd00'], 'Fresh boundary native state')
        registers = bytearray.fromhex(case['result']['registerFileBeforeHex'])
        require(len(registers) == 1024, 'Boundary complete register file')
        invocation(case['result'], initial, registers, observed[2:], start, limit, enabled, 0)
        require(len(observed) == case['actualReturningCalls'], 'Boundary actual native return count')
        calls += len(observed)
    require(calls == controls['boundaryControlActualReturningCalls'] == report['separateBoundaryControlNativeReturns'], 'Separate boundary-control returns')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Local pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(node.value) for node in ast.parse(path.read_text()).body if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in node.targets))
    for name, pin in pins.items():
        checked(root, {'path': name, 'sha256': pin})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_runtime_flags_frozen_matcher')
    require(matcher.ROOT == matcher.assets.ROOT == matcher.fixtures.native.ROOT == root, 'Local input imports')
    matcher.assets.original_files.cache_clear()
    for name, pin in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
                      ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH), ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': pin})
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH
            and report['sourceClosure'] == [{'path': n, 'sha256': p} for n, p in pins.items()], 'Frozen source/generator closure')
    data = matcher.assets.load(root / 'extract/files/world.e')
    rom, files = matcher.assets.original_files()
    raw, interval = (root / data['asset']).read_bytes(), files['world.e']
    require(raw == rom[interval[0]:interval[1]] and report['romSha256'] == matcher.assets.ROM_HASH and report['romFileRange'] == list(interval)
            and report['archiveSha256'] == data['assetSha256'] and report['scriptSha256'] == data['scriptSha256']
            and report['codeSha256'] == digest(data['code']), 'Current ROM/archive/image identity')
    require(report['boundariesAndStorage'] == matcher.boundary(data), 'Complete direct/private bounds, slot audit and unreachable join')
    build = report['sourceOnlyBuild']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False and build['cwd'] ==
            str(root / 'work/script-source/20261030/batch12/runtime-flags/source-only') and build['command'] ==
            [sys.executable, 'scr_c_compiler_20261030_v10.py', '--source', 'clear_primary_range_450_498.c', '--base', hex(BASE),
             '--locals', 'range.locals.json', '--output', 'generated.scrfunc', '--report', 'build.json'], 'Actual source-only command/directory')
    inputs = {Path(item['path']).name: checked(root, item) for item in build['inputs']}
    expected = {'scr_c_compiler_20261029.py', 'scr_c_compiler_20261030_v10.py', 'clear_primary_range_450_498.c', 'scr_runtime_flags.h', 'range.locals.json'}
    require(set(inputs) == expected and len(build['inputs']) == 5, 'Exact source-only closure')
    for filename, p in inputs.items():
        origin = filename if filename.endswith('.py') else 'src/scripts/20261030/batch12/' + filename
        require(digest(p.read_bytes()) == pins[origin], 'Copied source/header/allocation/compiler identity')
    body = checked(root, build['emittedBody']).read_bytes()
    evidence = json.loads(checked(root, build['compilerReport']).read_text())
    require(body == data['code'][BASE:END] and evidence == build['compilerEvidence'] and evidence['runtimeLoop'] is True
            and evidence['constantLoopUnrolled'] is False and evidence['entryNonemptyConditionStaticallyProven'] is True
            and evidence['counter']['sourceType'] == 'int' and evidence['counter']['allIntegerValuesExactlyRepresentable'] is True,
            'Actual220B C runtime loop/exact integer domain')
    stage = root / 'work/script-source/20261030/batch12/validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for filename, p in inputs.items():
            shutil.copyfile(p, directory / filename)
        subprocess.run(build['command'], cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        require((directory / 'generated.scrfunc').read_bytes() == body and json.loads((directory / 'build.json').read_text()) == evidence,
                'Fresh isolated source-only rebuild')
    require(report['matchedRange'] == {'startPc': BASE, 'endExclusivePc': END, 'bytes': 220, 'sha256': digest(body)}
            and checked(root, build['rebuiltImage']).read_bytes() == data['script'], 'Complete source range/current rebuilt image')
    controls(matcher, report)
    native_proof(report)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1 and report['qualifiedScriptRangeBytes'] == 220
            and report['originalScaffoldingBytes'] == len(data['script']) - 220, 'Source unit scope')
    require(all(report[key] == 0 for key in ('scaffoldingSourceCredit', 'nativeExecutableByteCredit', 'completeImagesRecovered', 'nativeFunctionStubs'))
            and report['postFaultStateUsedForProof'] is False and report['wholeRomSourceMatch'] is False
            and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'No excess credit/post-fault proof')
    key = digest(data['code']), BASE
    return {key: {'codeSha256': key[0], 'scriptSha256': data['scriptSha256'], 'asset': data['asset'], 'startPc': BASE,
        'endExclusivePc': END, 'bytes': 220, 'sha256': digest(body), 'mode': 'SCR', 'vmHostProcessor': 'ARM9', 'entryAliases': [257],
        'source': 'src/scripts/20261030/batch12/clear_primary_range_450_498.c', 'sourceSha256': evidence['sourceSha256'],
        'sourceDefinitionCount': 1, 'substantiveRuntimeLoopBytes': 220, 'pairedCompleteOwnEntryExecutions': 64,
        'pairedNativeReturningCalls': report['pairedNativeReturningCalls'], 'pairedPrimarySetterExecutions': 3136,
        'compilerGeneratedUnreachableJoinBytes': 12, 'wholeImageReconstructed': False}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(u['bytes'] for u in units.values())}))
