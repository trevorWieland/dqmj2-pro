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
    raise ValueError('Frozen helper')
spec = importlib.util.spec_from_file_location('_world17_shared', SHARED)
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_world17_20261030_batch11.py'
MATCHER_HASH = 'b405d19b31a6a5d85f1c66ba2ec3fee66410482a7c34d6bed352bd65b3d0d1ff'
REPORT = 'evidence/matches/scripts-20261030-world17.json'
BASE, END = 59076, 60224
PERSIST, NUMERIC, PRIMARY = 0x021B9EB4, 0x021C0DC8, 0x021C0E20
VALUES = (6, 19, 31, 43, 49, 59)


def word(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def floating(value):
    return struct.unpack('<f', struct.pack('<I', value))[0]


def get_bit(state, index):
    return bool(state[PRIMARY + index // 8 - PERSIST] & (1 << (index & 7)))


def set_bit(state, index, value):
    offset, mask = PRIMARY + index // 8 - PERSIST, 1 << (index & 7)
    state[offset] = state[offset] | mask if value else state[offset] & ~mask


def population():
    inverse = pow(0x41C64E6D, -1, 1 << 32)
    gated = [(a, b, n, 0, 255, t) for a, b in ((False, False), (False, True), (True, True))
             for n in (0, 4, 8, 255) for t in range(4)]
    choices = [(True, False, n, ((r * 65536 - 0x3039) * inverse) % (1 << 32), 255 if r & 1 else VALUES[r], t)
               for n in (0, 3, 4, 7, 8, 255) for r in range(6) for t in range(4)]
    return gated + choices


def domain_exclusion(data):
    rows = {row['pc']: row for row in data['instructions']}
    require(rows[59540]['opcode'] == 1045 and rows[59540]['argumentsRaw'][1:] == [1, 0, 2, word(6)]
            and rows[59564]['opcode'] == 36 and rows[59572]['argumentsRaw'][1:] == [0, word(98), 1, 0],
            'Actual native bound6 call and raw result storage')
    remaining = set(range(6))
    comparisons = [59596, 59700, 59804, 59908, 60012, 60116]
    for value, pc in enumerate(comparisons):
        require(rows[pc]['opcode'] == 1039 and rows[pc]['argumentsRaw'][1:] == [0, word(98), 2, word(value)],
                'Actual ordered equality exclusions')
        branch = rows[pc + 24]
        require(branch['opcode'] == 1038 and branch['argumentsRaw'][1] == (comparisons[value + 1] if value < 5 else END - 4),
                'False edge reaches next equality or private return')
        require(rows[pc + 92]['opcode'] == 1036 and rows[pc + 92]['argumentsRaw'][1] == END - 4,
                'Successful selection cannot enter subsequent comparisons')
        if value == 5:
            require(remaining == {5}, 'No valid final false RNG value remains')
        remaining.discard(value)
    require(not remaining, 'Complete bounded six-way selection')


def invocation(part, before, registers, rng, decoded, observations):
    pc, args, condition = BASE, {}, False
    state, operations = bytearray(before), []
    enabled, blocked = get_bit(before, 93), get_bit(before, 28)
    old32 = before[NUMERIC + 32 - PERSIST]
    selected, following = None, rng
    if enabled and not blocked:
        if old32 < 4:
            operations.append([32, 4])
        if old32 < 8:
            following = (rng * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
            selected = (following >> 16) % 6
            operations.append([31, VALUES[selected]])
    require(part['registerFileBeforeHex'] == bytes(registers).hex(), 'Exact whole register-file carry')
    require(len(part['trace']) == len(observations), 'One actual native return per executed record')
    getters, setters, stores, random_calls, branches = [], [], [], [], []
    for step, observed in zip(part['trace'], observations):
        row = decoded[pc]
        op, x = row['opcode'], row['argumentsRaw']
        require(step['pc'] == pc and step['opcode'] == op and BASE <= pc < END, 'Exact current record')
        next_pc = pc + row['bytes']
        def read(mode, raw):
            if mode == 2:
                return raw
            slot = int(floating(raw))
            require(mode in (0, 1), 'Scalar operand mode')
            return struct.unpack_from('<I', registers, slot * 4)[0] if mode == 0 else args[slot]
        if op == 1045:
            value, slot = read(x[3], x[4]), int(floating(x[2]))
            if x[1] == 0:
                struct.pack_into('<I', registers, slot * 4, value)
            else:
                require(x[1] == 1, 'Argument destination')
                args[slot] = value
        elif op in (1039, 1042, 1044):
            left, right = floating(read(x[1], x[2])), floating(read(x[3], x[4]))
            condition = left == right if op == 1039 else left < right if op == 1042 else left <= right
        elif op == 1036:
            next_pc = x[1]
        elif op == 1038:
            branches.append({'pc': pc, 'value': condition})
            next_pc = next_pc if condition else x[1]
        elif op in (39, 40, 41):
            index = int(floating(args[0]))
            previous = int(get_bit(state, index)) if op == 41 else state[NUMERIC + index - PERSIST]
            if op == 40:
                value = int(floating(args[1]))
                require(index in (31, 32), 'Only two supported numeric writes')
                setters.append([index, value])
                state[NUMERIC + index - PERSIST] = value
                stores.append({'address': hex(NUMERIC + index), 'bytes': 1, 'value': value})
            else:
                getters.append({'pc': pc, 'kind': 'primary' if op == 41 else 'numeric', 'index': index, 'value': previous})
            args[0] = word(previous)
        elif op == 36:
            require(floating(args[0]) == 6 and selected is not None and 0 <= selected < 6, 'Genuine bounded random API domain')
            random_calls.append({'pc': pc, 'bound': 6, 'before': rng, 'after': following, 'selection': selected})
            args[0] = word(selected)
        else:
            require(op == 1026 and pc == END - 4, 'Sole private return')
            next_pc = pc
        require(step['nextPc'] == next_pc and observed['persistentSha256'] == digest(state), 'Branch and full per-step persistent state')
        require(observed['entry'] == ('0x205a65c' if op < 1024 else '0x204c5a0') and observed['resultWord'] == 1,
                'Actual native dispatcher result')
        pc = next_pc
    require(pc == END - 4 and part['trace'][-1]['opcode'] == 1026 and part['completeEntry17Returned'] is True, 'Complete own entry return')
    require(part['setters'] == setters == operations and part['getters'] == getters and part['randomCalls'] == random_calls
            and part['persistentStores'] == stores and part['branches'] == branches, 'Independent complete semantic effects')
    require(part['rngBefore'] == rng and part['rngAfter'] == following and part['selection'] == selected
            and part['numeric32Before'] == old32 and part['primary93'] == enabled and part['primary28'] == blocked, 'Typed inputs/domain/RNG effects')
    require(part['persistentBeforeSha256'] == digest(before) and part['persistentAfterSha256'] == digest(state)
            and part['registerFileAfterSha256'] == digest(registers) and part['allOtherSlotsPreserved'] is True
            and part['onlyNumeric31And32MayChange'] is True, 'Whole persistent/register-file effects')
    return bytes(state), following


def native_proof(report, data):
    proof, inputs = report['differential'], population()
    require(len(proof['cases']) == len(inputs) == 192 and proof['nativeInstructionCap'] == 20000
            and proof['nativeTimeoutMicroseconds'] == 1000000 and proof['scriptStepBound'] == 80
            and proof['serializedCompleteCallsOnly'] is True and proof['naturalSceneOrRenewabilityMeaningProven'] is False, 'Execution population/scope')
    decoded, calls, coverage, executed, selections = {r['pc']: r for r in data['instructions']}, 0, {}, set(), set()
    for index, (case, values) in enumerate(zip(proof['cases'], inputs)):
        enabled, blocked, number32, rng, number31, thread = values
        seed = 2026103017000 + index
        require({k: case[k] for k in ('seed', 'thread', 'primary93', 'primary28', 'numeric32', 'rngSeed', 'numeric31')} ==
                {'seed': seed, 'thread': thread, 'primary93': enabled, 'primary28': blocked,
                 'numeric32': number32, 'rngSeed': rng, 'numeric31': number31}, 'Exact fresh-machine scenarios')
        state = bytearray(random.Random(seed).randbytes(0x7040))
        state[NUMERIC + 31 - PERSIST], state[NUMERIC + 32 - PERSIST] = number31, number32
        set_bit(state, 93, enabled)
        set_bit(state, 28, blocked)
        registers = bytearray(random.Random(seed ^ 0xB17).randbytes(1024))
        observed = case['observations']
        shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([v['entry'] for v in observed[:len(startup)]] == startup
                and all(v['persistentSha256'] == digest(state) for v in observed[:len(startup)]), 'Native fresh init/start/forks')
        cursor = len(startup)
        for ordinal, key in enumerate(('first', 'second')):
            if ordinal:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0')
                        and observed[cursor]['persistentSha256'] == digest(state), 'Natural serialized reentry')
                cursor += 1
            part = case[key]
            end = cursor + len(part['trace'])
            state, rng = invocation(part, state, registers, rng, decoded, observed[cursor:end])
            executed.update(s['pc'] for s in part['trace'])
            if part['selection'] is not None:
                selections.add(part['selection'])
            for branch in part['branches']:
                coverage.setdefault(branch['pc'], set()).add(branch['value'])
            cursor = end
        require(cursor == len(observed) == case['actualReturningCalls'], 'Exact returning-call population')
        calls += cursor
    require(proof['branchCoverage'] == {str(k): sorted(v) for k, v in coverage.items()} and len(coverage) == 10
            and coverage[60140] == {True} and all(v == {False, True} for k, v in coverage.items() if k != 60140), 'All feasible branch outcomes')
    require(selections == set(range(6)) and proof['allSixSelections'] == list(range(6))
            and proof['lastComparisonFalseExcludedByNativeRandomDomain'] is True and proof['nativeRandomBound'] == 6, 'All genuine choices/domain exclusion')
    require(executed == set(report['boundariesAndStorage']['reachableOwnRecordPcs'])
            and report['executedOwnRecordPcs'] == sorted(executed) and report['allReachableOwnRecordsExecuted'] is True
            and report['unreachableCompilerJoinRecordsNotForced'] is True, 'Only reachable entry-domain records executed')
    require(report['excludedBranchOutcomes'] == [{'pc': 60140, 'excludedValue': False, 'nativeBound': 6,
        'selectionDomain': [0, 1, 2, 3, 4, 5], 'earlierFalseEqualities': [0, 1, 2, 3, 4], 'remainingDomain': [5], 'outOfDomainRngInjected': False}],
        'Explicit impossible outcome and no injected result')
    require(calls == proof['actualReturningCalls'] and report['pairedNativeReturningCalls'] == calls * 2
            and proof['freshMachines'] == 192 and report['pairedCompleteOwnEntryExecutions'] == 768, 'Separate native/complete-entry totals')


def controls(matcher, report):
    evidence = report['compilerControls']
    require(len(evidence['rejectedSourceProfiles']) == 10 and evidence['syntheticControlSourceCredit'] == 0
            and evidence['arbitraryContextFloatOrderingSupportClaimed'] is False, 'Negative source and byte-domain scope')
    for item in evidence['rejectedSourceProfiles']:
        source = checked(ROOT, item['source'])
        require((source.parent / 'scr_random_decision.h').read_bytes() == (matcher.SOURCE / 'scr_random_decision.h').read_bytes(), 'Control include closure')
        try:
            matcher.compiler.compile_source(source, BASE, item['bindings'])
        except ValueError as error:
            require(str(error) == item['error'] and item['rejectedBeforeOutput'] is True, 'Current source/profile rejection')
        else:
            raise ValueError('Unsupported random-decision source compiles')
    source = checked(ROOT, evidence['byteRelationSource'])
    body, build = matcher.compiler.compile_source(source, 0, {'locals': {'value': 96}, 'globals': {}})
    require(len(body) == 280 and json.loads(json.dumps(build)) == evidence['byteRelationBuild'], 'Actual byte-domain source rebuild')
    require(len(evidence['all256ByteRelationCases']) == 256, 'Exhaustive byte comparisons')
    calls = 0
    for value, case in enumerate(evidence['all256ByteRelationCases']):
        require(case['numeric32'] == value and case['numeric30'] == (1 if value < 4 else 2 if value >= 8 else 0)
                and case['controlActuallyReturned'] is True and case['sourceCredit'] == 0, 'Independent byte truth table')
        pcs = [0, 12, 36, 44, 68, 92] + ([104, 128, 152, 160] if value < 4 else []) + [172, 196]
        pcs += ([208, 232, 256, 264] if value >= 8 else []) + [276]
        ops = [1036, 1045, 39, 1045, 1042, 1038] + ([1045, 1045, 40, 1036] if value < 4 else []) + [1044, 1038]
        ops += ([1045, 1045, 40, 1036] if value >= 8 else []) + [1026]
        require(case['trace'] == [{'pc': pc, 'opcode': op, 'nextPc': pcs[i + 1] if i + 1 < len(pcs) else pc}
                for i, (pc, op) in enumerate(zip(pcs, ops))], 'Byte-control branch/private return')
        observed = case['observations']
        shared.observations(observed)
        require([v['entry'] for v in observed] == ['0x204bc08', '0x204bd00'] +
                ['0x205a65c' if op < 1024 else '0x204c5a0' for op in ops]
                and len(observed) == case['actualReturningCalls'], 'Actual control native returns')
        state = bytearray(random.Random(2026103019000 + value).randbytes(0x7040))
        state[NUMERIC + 32 - PERSIST], state[NUMERIC + 30 - PERSIST] = value, 0
        require(observed[0]['persistentSha256'] == digest(state), 'Control initial state')
        state[NUMERIC + 30 - PERSIST] = case['numeric30']
        require(observed[-1]['persistentSha256'] == digest(state), 'Control complete effect')
        calls += len(observed)
    require(calls == evidence['byteRelationActualReturningCalls'] == report['syntheticByteControlNativeReturns'] == 3824, 'Separate synthetic return total')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Local pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(n.value) for n in ast.parse(path.read_text()).body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in n.targets))
    for name, sha in pins.items():
        checked(root, {'path': name, 'sha256': sha})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_world17_frozen_matcher')
    require(matcher.ROOT == matcher.assets.ROOT == matcher.fixtures.native.ROOT == root, 'Local input imports')
    matcher.assets.original_files.cache_clear()
    for name, sha in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
                      ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH), ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': sha})
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH
            and report['sourceClosure'] == [{'path': p, 'sha256': s} for p, s in pins.items()], 'Frozen source/generator closure')
    data = matcher.assets.load(root / 'extract/files/world.e')
    rom, files = matcher.assets.original_files()
    raw, interval = (root / data['asset']).read_bytes(), files['world.e']
    require(raw == rom[interval[0]:interval[1]] and report['romSha256'] == matcher.assets.ROM_HASH and report['romFileRange'] == list(interval)
            and report['archiveSha256'] == data['assetSha256'] and report['scriptSha256'] == data['scriptSha256']
            and report['codeSha256'] == digest(data['code']), 'Current ROM/archive/image')
    profile = json.loads((matcher.SOURCE / 'selection.bindings.json').read_text())
    require(report['boundariesAndStorage'] == matcher.boundary(data, profile), 'Current direct/private bounds, slots and unreachable CFG')
    build = report['sourceOnlyBuild']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False, 'Source-only compiler invocation')
    require(build['cwd'] == str(root / 'work/script-source/20261030/batch11/world17/source-only') and build['command'] ==
            [sys.executable, 'scr_c_compiler_20261030_v9.py', '--source', 'select_numeric_thirty_one.c', '--base', hex(BASE),
             '--bindings', 'selection.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json'],
            'Actual source-only command/directory')
    inputs = {Path(item['path']).name: checked(root, item) for item in build['inputs']}
    expected = {'scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py', 'scr_c_compiler_20261030_v6.py',
                'scr_c_compiler_20261030_v9.py', 'select_numeric_thirty_one.c', 'scr_random_decision.h', 'selection.bindings.json'}
    require(set(inputs) == expected and len(build['inputs']) == 7, 'Complete source-only input closure')
    for filename, p in inputs.items():
        origin = filename if filename.endswith('.py') else 'src/scripts/20261030/batch11/' + filename
        require(digest(p.read_bytes()) == pins[origin], 'Current copied source/header/profile/compiler identity')
    body = checked(root, build['emittedBody']).read_bytes()
    compiler_report = json.loads(checked(root, build['compilerReport']).read_text())
    require(body == data['code'][BASE:END] and compiler_report == build['compilerEvidence'], 'Full1148B actual product')
    require(compiler_report['earlyReturnBranches'] == [59180, 59296, 59516], 'Computed early-return branches')
    stage = root / 'work/script-source/20261030/batch11/validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for filename, p in inputs.items():
            shutil.copyfile(p, directory / filename)
        subprocess.run(build['command'], cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        require((directory / 'generated.scrfunc').read_bytes() == body and json.loads((directory / 'build.json').read_text()) == compiler_report,
                'Fresh isolated source-only re-emission')
    require(checked(root, build['rebuiltImage']).read_bytes() == data['script'] and report['matchedRange'] ==
            {'startPc': BASE, 'endExclusivePc': END, 'bytes': 1148, 'sha256': digest(body)}, 'Current rebuilt image and complete range')
    controls(matcher, report)
    domain_exclusion(data)
    native_proof(report, data)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1 and report['qualifiedScriptRangeBytes'] == 1148
            and report['originalScaffoldingBytes'] == len(data['script']) - 1148, 'Source unit population')
    for key in ('nativeExecutableByteCredit', 'scaffoldingSourceCredit', 'completeImagesRecovered', 'nativeFunctionStubs'):
        require(report[key] == 0, 'Zero excess credit: ' + key)
    require(report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True
            and report['postFaultStateUsedForProof'] is False and report['wholeRomSourceMatch'] is False, 'Evidence scope')
    key = digest(data['code']), BASE
    return {key: {'codeSha256': key[0], 'scriptSha256': data['scriptSha256'], 'asset': data['asset'], 'startPc': BASE,
        'endExclusivePc': END, 'bytes': 1148, 'sha256': digest(body), 'mode': 'SCR', 'vmHostProcessor': 'ARM9',
        'entryAliases': [17], 'source': 'src/scripts/20261030/batch11/select_numeric_thirty_one.c',
        'sourceSha256': compiler_report['sourceSha256'], 'sourceDefinitionCount': 1, 'substantiveDecisionLogicBytes': 1148,
        'pairedNativeReturningCalls': report['pairedNativeReturningCalls'], 'pairedCompleteOwnEntryExecutions': 768,
        'syntheticByteControlNativeReturns': 3824, 'compilerGeneratedUnreachableJoinBytes': 36,
        'excludedLastFalseRandomOutcome': True, 'wholeImageReconstructed': False}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(u['bytes'] for u in units.values())}))
