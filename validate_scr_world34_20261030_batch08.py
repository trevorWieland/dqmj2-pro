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
    raise ValueError('Frozen shared validation helper')
spec = importlib.util.spec_from_file_location('_world34_shared', SHARED)
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_world34_20261030_batch08.py'
MATCHER_HASH = '9f5d19e22eaca679d53e9cfbafe7bd93d9ecb20cfc1bd194ae006a097dacd259'
REPORT = 'evidence/matches/scripts-20261030-world34.json'
BASE, END = 64268, 65620
PERSIST, NUMERIC, PRIMARY = 0x021B9EB4, 0x021C0DC8, 0x021C0E20


def word(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def floating(value):
    return struct.unpack('<f', struct.pack('<I', value))[0]


def get_bit(state, index):
    return bool(state[PRIMARY + index // 8 - PERSIST] & (1 << (index & 7)))


def set_bit(state, index, value):
    offset, mask = PRIMARY + index // 8 - PERSIST, 1 << (index & 7)
    state[offset] = state[offset] | mask if value else state[offset] & ~mask


def expected_actions(state):
    number = lambda index: state[NUMERIC + index - PERSIST]
    operations = []
    if number(0) == 1 and number(4) == 15:
        operations += [('numeric', 0, 2), ('numeric', 4, 0), ('primary', 8, 1)]
    elif number(0) == 3:
        if number(4) == 1:
            operations += [('numeric', 4, 2), ('primary', 8, 1)]
        if number(5) == 7:
            operations += [('numeric', 5, 8)]
    if number(20) >= 28 and get_bit(state, 218) and number(28) == 5:
        operations += [('primary', 237, 1), ('primary', 203, 0)]
    return [list(item) for item in operations]


def invocation(part, before, registers, decoded, observations):
    state, pc, condition, args = bytearray(before), BASE, False, {}
    operations, getters, branches, stores = [], [], [], []
    expected_operations = expected_actions(state)
    require(len(part['trace']) == len(observations), 'One native return per SCR record')
    for step, observed in zip(part['trace'], observations):
        row = decoded[pc]
        opcode, operands = row['opcode'], row['argumentsRaw']
        require(step['pc'] == pc and step['opcode'] == opcode and BASE <= pc < END, 'Exact original trace identity')
        next_pc = pc + row['bytes']
        def read(mode, raw):
            if mode == 2:
                return raw
            slot = int(floating(raw))
            require(mode in (0, 1), 'World routine operand modes')
            return struct.unpack_from('<I', registers, slot * 4)[0] if mode == 0 else args[slot]
        if opcode == 1045:
            value = read(operands[3], operands[4])
            slot = int(floating(operands[2]))
            if operands[1] == 0:
                struct.pack_into('<I', registers, slot * 4, value)
            else:
                require(operands[1] == 1, 'Argument destination ABI')
                args[slot] = value
        elif opcode in (1039, 1043):
            left, right = floating(read(operands[1], operands[2])), floating(read(operands[3], operands[4]))
            condition = left == right if opcode == 1039 else left >= right
        elif opcode == 1036:
            next_pc = operands[1]
        elif opcode == 1038:
            branches.append({'pc': pc, 'value': condition})
            next_pc = next_pc if condition else operands[1]
        elif opcode == 1026:
            require(pc == END - 4, 'Sole private RET')
            next_pc = pc
        else:
            require(opcode in (39, 40, 41, 42), 'Only four named state APIs')
            index = int(floating(args[0]))
            numeric = opcode in (39, 40)
            previous = state[NUMERIC + index - PERSIST] if numeric else int(get_bit(state, index))
            kind = 'numeric' if numeric else 'primary'
            if opcode in (40, 42):
                value = int(floating(args[1]))
                operations.append([kind, index, value])
                if numeric:
                    state[NUMERIC + index - PERSIST] = value
                    stores.append({'address': hex(NUMERIC + index), 'bytes': 1, 'value': value})
                else:
                    set_bit(state, index, value)
                    address = PRIMARY + (index >> 5) * 4
                    stores.append({'address': hex(address), 'bytes': 4,
                                   'value': struct.unpack_from('<I', state, address - PERSIST)[0]})
            else:
                getters.append({'kind': kind, 'index': index, 'value': previous})
            args[0] = word(previous)
        require(step['nextPc'] == next_pc and observed['persistentSha256'] == digest(state), 'Branch and per-step full state')
        require(observed['entry'] == ('0x205a65c' if opcode < 1024 else '0x204c5a0') and observed['resultWord'] == 1,
                'Actual named dispatcher return')
        pc = next_pc
    require(part['trace'][-1]['opcode'] == 1026 and pc == END - 4 and part['completeEntry34Returned'] is True,
            'Whole entry termination')
    require(operations == expected_operations == part['setterOperations'] and getters == part['getters'], 'Independent high-level effects')
    require(part['branches'] == branches and part['persistentStores'] == stores, 'All branches and ordered byte/word stores')
    require(part['persistentBeforeSha256'] == digest(before) and part['persistentAfterSha256'] == digest(state), 'Full persistent bounds')
    require(part['completeRegisterFileSha256'] == digest(registers) and part['allOtherSlotsPreserved'] is True, 'Whole256-slot file')
    require(part['moduleGlobalWords'] == {'cached_numeric_twenty': word(before[NUMERIC + 20 - PERSIST]),
        'cached_numeric_twenty_eight': word(before[NUMERIC + 28 - PERSIST]), 'cached_primary_236': word(int(get_bit(before, 236)))},
        'Retained module objects, separate from private local storage')
    require(part['finalMutableStateWord'] == struct.unpack_from('<I', registers, 105 * 4)[0], 'Mutable local scalar result')
    return bytes(state)


def native_proof(report, data):
    proof = report['differential']
    require(proof['nativeInstructionCap'] == 20000 and proof['nativeTimeoutMicroseconds'] == 1000000
            and proof['scriptStepBound'] == 96 and proof['serializedCompleteCallsOnly'] is True, 'Execution scope/caps')
    require(proof['moduleGlobalsRemainObservableAfterReturn'] is True, 'Global lifetime proof')
    phases = [(1, 15, 0), (1, 14, 7), (3, 1, 7), (3, 1, 6), (3, 0, 7), (3, 0, 0), (0, 255, 255), (255, 0, 0)]
    gates = [(27, 5, True), (28, 5, False), (28, 4, True), (28, 5, True)]
    inputs = [(a, b, c, d, e, f, t) for a, b, c in phases for d, e, f in gates for t in range(4)]
    require(len(proof['cases']) == len(inputs) == 128, 'Complete cases/all4threads')
    decoded = {row['pc']: row for row in data['instructions']}
    calls, coverage, executed = 0, {}, set()
    for index, (case, values) in enumerate(zip(proof['cases'], inputs)):
        zero, four, five, twenty, twenty_eight, flag, thread = values
        seed, pattern = 2026103008001 + index, (index + (index // 16) * 7) % 16
        require(case['seed'] == seed and case['thread'] == thread and case['inputs'] == {'numeric0': zero,
            'numeric4': four, 'numeric5': five, 'numeric20': twenty, 'numeric28': twenty_eight,
            'primary218': flag, 'initialFlagPattern': pattern}, 'Scenario identity')
        require(case['unknownControlHalfwordNotOverridden'] is True, 'No fabricated auxiliary state prerequisite')
        state = bytearray(random.Random(seed).randbytes(0x7040))
        for slot, value in ((0, zero), (4, four), (5, five), (20, twenty), (28, twenty_eight)):
            state[NUMERIC + slot - PERSIST] = value
        for position, flag_index in enumerate((8, 203, 236, 237)):
            set_bit(state, flag_index, bool(pattern & (1 << position)))
        set_bit(state, 218, flag)
        initial, control = bytes(state), state[0x021C0ECC - PERSIST:0x021C0ECE - PERSIST]
        registers = bytearray(random.Random(seed ^ 0x835).randbytes(1024))
        observations = case['observations']
        shared.observations(observations)
        start = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([item['entry'] for item in observations[:len(start)]] == start
                and all(item['persistentSha256'] == digest(initial) for item in observations[:len(start)]), 'Fresh init/start/thread calls')
        cursor = len(start)
        for part_index, label in enumerate(('first', 'second')):
            if part_index:
                item = observations[cursor]
                require(item['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0')
                        and item['persistentSha256'] == digest(state), 'Natural serialized reentry')
                cursor += 1
            part = case[label]
            end = cursor + len(part['trace'])
            state = invocation(part, state, registers, decoded, observations[cursor:end])
            cursor = end
            for branch in part['branches']:
                coverage.setdefault(branch['pc'], set()).add(branch['value'])
            executed.update(step['pc'] for step in part['trace'])
        require(cursor == len(observations) == case['actualReturningCalls']
                and state[0x021C0ECC - PERSIST:0x021C0ECE - PERSIST] == control, 'Call population and auxiliary preservation')
        calls += cursor
    expected_coverage = {str(pc): sorted(values) for pc, values in coverage.items()}
    require(proof['branchCoverage'] == expected_coverage and len(coverage) == 8
            and all(values == {False, True} for values in coverage.values())
            and proof['allEightBranchSitesHaveBothOutcomes'] is True, 'Every own branch outcome')
    require(executed == {pc for pc in decoded if BASE <= pc < END} and report['executedRecordPcs'] == sorted(executed)
            and report['allOwnRecordsExecuted'] is True, 'Every own record executed')
    require(calls == proof['actualReturningCalls'] == report['actualReturningCallsPerImplementation'] == 10176
            and report['actualReturningCallsTotal'] == 20352 and proof['freshMachines'] == report['freshMachinesPerImplementation'] == 128,
            'Fresh machine/paired return totals')


def compiler_controls(matcher, report):
    control = report['compilerControls']
    require(len(control['rejectedSourceProfiles']) == 12, 'Negative source/profile population')
    for item in control['rejectedSourceProfiles']:
        source = checked(ROOT, item['source'])
        require((source.parent / 'scr_world_state.h').read_bytes() == (matcher.SOURCE / 'scr_world_state.h').read_bytes(), 'Control include identity')
        try:
            matcher.compiler.compile_source(source, BASE, item['bindings'])
        except ValueError as error:
            require(str(error) == item['error'] and item['rejectedBeforeOutput'] is True, 'Reproducible rejection')
        else:
            raise ValueError('Rejected source now compiles')
    source = checked(ROOT, control['syntheticOrderedSource'])
    body, build = matcher.compiler.compile_source(source, 0, {'locals': {'state': 105}, 'globals': {}})
    require(json.loads(json.dumps(build)) == control['syntheticOrderedBuild'] and len(body) == 176 and control['syntheticControlSourceCredit'] == 0
            and control['orderedArbitraryContextFloatSupportClaimed'] is False, 'Separate byte-domain compiler control')
    require(len(control['all256ByteValues']) == 256, 'Exhaustive numeric-byte domain')
    calls = 0
    for value, case in enumerate(control['all256ByteValues']):
        require(case['numeric20'] == value and case['predicate'] == (value >= 28) and case['sourceCredit'] == 0
                and case['originalBytecodeInput'] is False and case['completeControlReturned'] is True, 'Ordered relation truth table')
        pcs = [0, 12, 36, 44, 68, 92] + ([104, 128, 152, 160] if value >= 28 else []) + [172]
        ops = [1036, 1045, 39, 1045, 1043, 1038] + ([1045, 1045, 42, 1036] if value >= 28 else []) + [1026]
        require(case['trace'] == [{'pc': pc, 'opcode': op, 'nextPc': pcs[i + 1] if i + 1 < len(pcs) else pc}
                for i, (pc, op) in enumerate(zip(pcs, ops))], 'Ordered control exact branches/private return')
        state = bytearray(random.Random(2026103009000 + value).randbytes(0x7040))
        state[NUMERIC + 20 - PERSIST] = value
        set_bit(state, 0, False)
        observed = case['observations']
        shared.observations(observed)
        require([item['entry'] for item in observed] == ['0x204bc08', '0x204bd00'] +
                ['0x205a65c' if op < 1024 else '0x204c5a0' for op in ops], 'Compiler-control native return order')
        require(observed[0]['persistentSha256'] == digest(state), 'Compiler-control initial state')
        set_bit(state, 0, value >= 28)
        require(observed[-1]['persistentSha256'] == digest(state) and len(observed) == case['actualReturningCalls'], 'Compiler-control final state')
        calls += len(observed)
    require(calls == control['orderedControlActualReturns'] == report['independentCompilerControlReturns'] == 3216, 'Separate control return total')


def caller_prefix(root, data):
    path = checked(root, {'path': 'evidence/encounter/guard-paths-20261029.json',
                         'sha256': '7a0b10d51dd7b95e630472f32c64c745d55a5e2a79df42eeb4461377ff50cac8'})
    prefix = json.loads(path.read_text())['worldEntryPrefix']
    require(prefix['scriptSha256'] == data['scriptSha256'] and prefix['assetSha256'] == data['assetSha256']
            and prefix['entryId'] == 128 and prefix['entryPc'] == data['entries'][128], 'Historical original prefix identity')
    trace = prefix['trace']
    for pc, target in ((50472, 60232), (63872, BASE), (END - 4, 63884), (63968, 50484)):
        require(len([row for row in trace if row['pc'] == pc and row['nextPc'] == target]) == 1, 'Measured original caller/return chain')
    require(prefix['unsupportedProbe']['countedAsReturningOrSupported'] is False
            and prefix['postFaultStateUsedForProof'] is False, 'Historical outer unsupported path excluded')
    return {'entryChain': [128, 32, 34], 'syntheticNumeric0': 4, 'syntheticNumeric1': 0,
            'historicalPrefixOnly': True, 'outerEntryReturnCredit': 0, 'additionalSourceCredit': 0}


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Repository identity/pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(node.value) for node in ast.parse(path.read_text()).body
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in node.targets))
    for name, sha in pins.items():
        checked(root, {'path': name, 'sha256': sha})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_world34_frozen_matcher')
    require(matcher.ROOT == matcher.assets.ROOT == matcher.fixtures.native.ROOT == root, 'Repository-local imports')
    matcher.assets.original_files.cache_clear()
    for name, sha in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
                      ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH),
                      ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': sha})
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH
            and report['sourceClosure'] == [{'path': name, 'sha256': sha} for name, sha in pins.items()], 'Frozen generator/source closure')
    data = matcher.assets.load(root / 'extract/files/world.e')
    rom, files = matcher.assets.original_files()
    raw, interval = (root / data['asset']).read_bytes(), files['world.e']
    require(raw == rom[interval[0]:interval[1]] and report['romSha256'] == matcher.assets.ROM_HASH
            and report['romFileRange'] == list(interval), 'Original ROM interval/hash')
    require(report['archiveSha256'] == data['assetSha256'] and report['scriptSha256'] == data['scriptSha256']
            and report['codeSha256'] == digest(data['code']), 'Current decoded image')
    members = []
    for index in range(matcher.assets.u32(raw, 4)):
        offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
        stored = raw[offset:offset + length]
        require(matcher.assets.ash(stored) == data['script'], 'Decoded archive alias')
        members.append({'index': index, 'offset': offset, 'bytes': length, 'storedSha256': digest(stored), 'scriptSha256': data['scriptSha256']})
    require(report['members'] == members and len(members) == 8, 'Alias population/no duplicate credit')
    profile = json.loads((matcher.SOURCE / 'world.bindings.json').read_text())
    require(report['boundariesAndModuleObjects'] == matcher.boundary(data, profile), 'Full bounds/module-global cross-entry qualification')
    require(report['namedNativeApiBindings'] == matcher.named_native_apis(), 'Four named native API identities')
    build = report['buildCommand']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False, 'Source-only build')
    executed_directory = root / 'work/script-source/20261030/batch08/world34/source-only'
    require(build['cwd'] == str(executed_directory) and build['command'] == [sys.executable,
            str(executed_directory / 'scr_c_compiler_20261030_v6.py'), '--source', 'advance_world_state.c',
            '--base', hex(BASE), '--bindings', 'world.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json'],
            'Actual source-only command/CWD identity')
    inputs = {Path(item['path']).name: checked(root, item) for item in build['inputs']}
    expected = {'scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py', 'scr_c_compiler_20261030_v6.py',
                'advance_world_state.c', 'scr_world_state.h', 'world.bindings.json'}
    require(set(inputs) == expected and len(build['inputs']) == 6, 'Complete source-only closure')
    for name, item in inputs.items():
        origin = name if name.endswith('.py') else 'src/scripts/20261030/batch08/' + name
        require(digest(item.read_bytes()) == pins[origin], 'Compiler/source/include/profile identity')
    body = checked(root, build['emittedBody']).read_bytes()
    source_report = json.loads(checked(root, build['compilerReport']).read_text())
    require(body == data['code'][BASE:END] and source_report == report['sourceOnlyBuild'], 'Full emitted body/compiler evidence')
    require(report['matchedRange'] == {'startPc': BASE, 'endExclusivePc': END, 'bytes': 1352, 'sha256': digest(body)}, 'Complete1352 gate')
    stage = root / 'work/script-source/20261030/batch08/validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for name, item in inputs.items():
            shutil.copyfile(item, directory / name)
        command = [sys.executable, 'scr_c_compiler_20261030_v6.py', '--source', 'advance_world_state.c', '--base', hex(BASE),
                   '--bindings', 'world.bindings.json', '--output', 'fresh.scrfunc', '--report', 'fresh.json']
        subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        require((directory / 'fresh.scrfunc').read_bytes() == body
                and json.loads((directory / 'fresh.json').read_text()) == source_report, 'Fresh isolated source-only re-emission')
    require(checked(root, build['rebuiltImage']).read_bytes() == data['script'], 'Current rebuilt decoded image')
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1
            and report['qualifiedScriptRangeBytes'] == 1352 and report['originalScaffoldingBytes'] == len(data['script']) - 1352, 'Unit population')
    for key in ('scaffoldingSourceCredit', 'completeImagesRecovered', 'nativeExecutableByteCredit', 'nativeFunctionStubs'):
        require(report[key] == 0, 'Zero extra credit: ' + key)
    require(report['wholeRomSourceMatch'] is False and report['postFaultStateUsedForProof'] is False
            and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'Proof scope')
    compiler_controls(matcher, report)
    native_proof(report, data)
    prefix = caller_prefix(root, data)
    key = digest(data['code']), BASE
    return {key: {'codeSha256': key[0], 'scriptSha256': data['scriptSha256'], 'asset': data['asset'],
        'startPc': BASE, 'endExclusivePc': END, 'bytes': 1352, 'sha256': digest(body), 'mode': 'SCR',
        'vmHostProcessor': 'ARM9', 'entryAliases': [34], 'source': 'src/scripts/20261030/batch08/advance_world_state.c',
        'sourceSha256': source_report['sourceSha256'], 'sourceDefinitionCount': 1, 'substantiveDecisionLogicBytes': 1352,
        'actualReturningCallsTotal': 20352, 'compilerControlReturns': 3216, 'wholeImageReconstructed': False,
        'moduleGlobalObjects': source_report['moduleGlobalObjects'], 'historicalCallerPrefix': prefix}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(unit['bytes'] for unit in units.values())}))
