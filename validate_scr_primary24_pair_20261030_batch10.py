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
    raise ValueError('Frozen shared validator')
spec = importlib.util.spec_from_file_location('_primary24_pair_shared', SHARED)
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_primary24_pair_20261030_batch10.py'
MATCHER_HASH = '1184cbc5a2ad6a0ada8947f5d43d9fde6eb9657a8300fd063a4bd370991706e2'
REPORT = 'evidence/matches/scripts-20261030-primary24-pair.json'
PERSIST, NUMERIC, PRIMARY = 0x021B9EB4, 0x021C0DC8, 0x021C0E20


def word(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def floating(value):
    return struct.unpack('<f', struct.pack('<I', value))[0]


def set_bit(state, value):
    state[PRIMARY + 3 - PERSIST] = state[PRIMARY + 3 - PERSIST] | 1 if value else state[PRIMARY + 3 - PERSIST] & 254


def population(kind):
    requests = (4, 5, 6) if kind == 'enable' else (7, 8, 9, 14, 15, 16)
    triples = [(word(request), zero, three) for request in requests for zero in (1, 2) for three in (5, 6, 8)]
    triples += [(bits, 2, 6) for bits in (0, 0x80000000, 0x7F800000, 0xFF800000, 0x7FC00001, 0xFFC00001,
                word(5 if kind == 'enable' else 8) - 1, word(5 if kind == 'enable' else 8) + 1)]
    triples += [(word(5 if kind == 'enable' else 15), zero, three) for zero, three in ((0, 6), (255, 6), (2, 0), (2, 255))]
    return [(bits, zero, three, flag, thread) for bits, zero, three in triples for flag in (False, True) for thread in range(4)]


def invocation(part, before, registers, input_word, kind, native_unit, decoded, observations):
    base, end = native_unit['base'], native_unit['end']
    state, pc, args, condition = bytearray(before), base, {0: input_word}, False
    zero, three = before[NUMERIC - PERSIST], before[NUMERIC + 3 - PERSIST]
    request = floating(input_word)
    entered = request == 5 if kind == 'enable' else request in (8, 15)
    success = zero == 2 and ((request == 5 and three == 6) if kind == 'enable' else
                           (request == 8 and three == 6 or request == 15 and three == 8))
    previous_state_slot = bytes(registers[native_unit['state'] * 4:native_unit['state'] * 4 + 4])
    getters, setters, stores, branches = [], [], [], []
    require(part['registerFileBeforeHex'] == bytes(registers).hex(), 'Exact register-file state carry')
    require(len(part['trace']) == len(observations), 'One native return per owned record')
    for step, observation in zip(part['trace'], observations):
        row = decoded[pc]
        opcode, x = row['opcode'], row['argumentsRaw']
        require(step['pc'] == pc and step['opcode'] == opcode and base <= pc < end, 'Current decoded own trace')
        next_pc = pc + row['bytes']
        def read(mode, raw):
            if mode == 2:
                return raw
            slot = int(floating(raw))
            require(mode in (0, 1), 'No direct context input in formal routine')
            return struct.unpack_from('<I', registers, slot * 4)[0] if mode == 0 else args[slot]
        if opcode == 1045:
            value, slot = read(x[3], x[4]), int(floating(x[2]))
            if x[1] == 0:
                struct.pack_into('<I', registers, slot * 4, value)
            else:
                require(x[1] == 1, 'Argument destination')
                args[slot] = value
        elif opcode == 1039:
            condition = floating(read(x[1], x[2])) == floating(read(x[3], x[4]))
        elif opcode == 1036:
            next_pc = x[1]
        elif opcode == 1038:
            branches.append({'pc': pc, 'value': condition})
            next_pc = next_pc if condition else x[1]
        elif opcode == 39:
            index = int(floating(args[0]))
            require(index in (0, 3), 'Numeric source identities')
            value = state[NUMERIC + index - PERSIST]
            getters.append({'pc': pc, 'index': index, 'value': value})
            args[0] = word(value)
        elif opcode == 42:
            require(floating(args[0]) == 24 and floating(args[1]) == int(kind == 'enable') and success, 'Primary24 setter ABI')
            previous = int(bool(state[PRIMARY + 3 - PERSIST] & 1))
            set_bit(state, kind == 'enable')
            setters.append({'pc': pc, 'index': 24, 'value': int(kind == 'enable')})
            stores.append({'address': hex(PRIMARY), 'bytes': 4, 'value': struct.unpack_from('<I', state, PRIMARY - PERSIST)[0]})
            args[0] = word(previous)
        else:
            require(opcode == 1026 and pc == end - 4, 'Sole private return')
            next_pc = pc
        require(step['nextPc'] == next_pc and observation['persistentSha256'] == digest(state), 'Exact branch/full persistent effect')
        require(observation['entry'] == ('0x205a65c' if opcode < 1024 else '0x204c5a0') and observation['resultWord'] == 1,
                'Actual native dispatcher result')
        pc = next_pc
    require(pc == end - 4 and part['trace'][-1]['opcode'] == 1026 and part['completeEntryReturned'] is True, 'Whole entry return')
    require(part['formalWord'] == input_word and part['numeric0'] == zero and part['numeric3'] == three, 'Typed formal/numeric inputs')
    require(part['getters'] == getters and part['setters'] == setters and part['persistentStores'] == stores
            and part['branches'] == branches and part['setterInvoked'] == success and len(setters) == int(success), 'Independent semantic operations')
    require(part['persistentBeforeSha256'] == digest(before) and part['persistentAfterSha256'] == digest(state)
            and part['persistentChanged'] == (bytes(before) != bytes(state)), 'Persistent boundaries')
    require(part['registerFileAfterSha256'] == digest(registers) and part['allOtherSlotsPreserved'] is True
            and part['unenteredStateSlotPreserved'] == (not entered), 'Entire256-slot effect including declaration without initializer')
    expected_scalar = word(three if zero == 2 else zero) if entered else struct.unpack('<I', previous_state_slot)[0]
    require(struct.unpack_from('<I', registers, native_unit['state'] * 4)[0] == expected_scalar
            and struct.unpack_from('<I', registers, native_unit['formal'] * 4)[0] == input_word, 'Definite assignment and raw formal word')
    return bytes(state)


def prefixes(proof, kind, native_unit, data):
    requests = (5,) if kind == 'enable' else (8, 15)
    require(len(proof['qualifiedCallerPrefixes']) == len(requests) and proof['prefixOuterEntryReturnCredit'] == 0
            and proof['prefixAdditionalSourceCredit'] == 0, 'Separately scoped caller prefixes')
    calls = 0
    for item, request in zip(proof['qualifiedCallerPrefixes'], requests):
        start = data['entries'][129]
        target_call = 119112 if kind == 'enable' else 101768
        require(item['request'] == request and item['entry'] == 129 and item['targetEntry'] == 102
                and item['targetCallPc'] == target_call and item['boundaryPc'] == target_call + 12
                and item['formalArgumentWordAtTarget'] == word(request), 'Context-to-formal producer identity')
        require(item['targetEntryActuallyReturned'] is True and item['outerEntryReturned'] is False
                and item['boundaryCountedAsOuterReturn'] is False and item['sourceCredit'] == 0
                and item['context0ProvidedSynthetically'] is True and item['nativeLauncherProducerProven'] is False, 'No outer/natural launch credit')
        trace = item['trace']
        require(trace[0]['pc'] == start and trace[-1] == {'pc': native_unit['end'] - 4, 'opcode': 1026, 'nextPc': target_call + 12},
                'Actual complete callee return inside incomplete outer prefix')
        require(any(s == {'pc': start + 36, 'opcode': 1033, 'nextPc': 49684} for s in trace)
                and any(s == {'pc': target_call, 'opcode': 1033, 'nextPc': native_unit['base']} for s in trace), 'Original helper and target calls executed')
        observed = item['observations']
        shared.observations(observed)
        require([s['entry'] for s in observed] == ['0x204bc08', '0x204bd00'] +
                ['0x205a65c' if s['opcode'] < 1024 else '0x204c5a0' for s in trace]
                and len(observed) == item['actualReturningCalls'], 'True prefix native returns')
        calls += len(observed)
    require(calls == proof['prefixActualReturningCalls'], 'Separate prefix returning population')
    return calls


def native_proof(unit_report, native_unit, data):
    proof, kind = unit_report['differential'], unit_report['kind']
    require(proof['nativeInstructionCap'] == 20000 and proof['nativeTimeoutMicroseconds'] == 1000000 and proof['scriptStepBound'] == 48
            and proof['formalArgumentProducerProvenByTheseCases'] is False and proof['serializedCompleteCallsOnly'] is True, 'Execution bounds/scope')
    inputs, calls, coverage, executed = population(kind), 0, {}, set()
    require(len(proof['cases']) == len(inputs), 'Complete branch/NaN/numeric/thread/initial-bit population')
    decoded = {r['pc']: r for r in data['instructions']}
    for index, (case, (input_word, zero, three, flag, thread)) in enumerate(zip(proof['cases'], inputs)):
        seed = (2026103011000 if kind == 'enable' else 2026103012000) + index
        require({k: case[k] for k in ('seed', 'thread', 'formalWord', 'numeric0', 'numeric3', 'initialPrimary24')} ==
                {'seed': seed, 'thread': thread, 'formalWord': input_word, 'numeric0': zero, 'numeric3': three, 'initialPrimary24': flag}
                and case['context0IsDistinctNinetyNine'] is True, 'Scenario identities')
        state = bytearray(random.Random(seed).randbytes(0x7040))
        state[NUMERIC - PERSIST], state[NUMERIC + 3 - PERSIST] = zero, three
        set_bit(state, flag)
        registers = bytearray(random.Random(seed ^ 0xA41).randbytes(1024))
        observed = case['observations']
        shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([r['entry'] for r in observed[:len(startup)]] == startup
                and all(r['persistentSha256'] == digest(state) for r in observed[:len(startup)]), 'Fresh init/start/forks')
        cursor = len(startup)
        for ordinal, key in enumerate(('first', 'second')):
            if ordinal:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0')
                        and observed[cursor]['persistentSha256'] == digest(state), 'Natural serialized reentry')
                cursor += 1
            part = case[key]
            end = cursor + len(part['trace'])
            state = invocation(part, state, registers, input_word, kind, native_unit, decoded, observed[cursor:end])
            executed.update(s['pc'] for s in part['trace'])
            for branch in part['branches']:
                coverage.setdefault(branch['pc'], set()).add(branch['value'])
            cursor = end
        require(cursor == len(observed) == case['actualReturningCalls'], 'Exact native return population')
        calls += cursor
    require(proof['branchCoverage'] == {str(k): sorted(v) for k, v in coverage.items()}
            and len(coverage) == (3 if kind == 'enable' else 6) and all(v == {False, True} for v in coverage.values())
            and proof['everyOwnBranchHasBothOutcomes'] is True, 'Every branch outcome')
    require(executed == {pc for pc in decoded if native_unit['base'] <= pc < native_unit['end']}
            and unit_report['executedOwnRecordPcs'] == sorted(executed) and unit_report['allOwnRecordsExecuted'] is True, 'Every owned record executed')
    require(calls == proof['actualReturningCalls'] and unit_report['pairedNativeReturningCalls'] == calls * 2
            and proof['freshMachines'] == len(inputs) and unit_report['pairedCompleteOwnEntryExecutions'] == len(inputs) * 4, 'Native versus complete-entry counts')
    prefix_calls = prefixes(proof, kind, native_unit, data)
    require(unit_report['prefixNativeReturningCalls'] == prefix_calls * 2, 'Paired prefix native returns')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Repository-local pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(n.value) for n in ast.parse(path.read_text()).body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in n.targets))
    for name, sha in pins.items():
        checked(root, {'path': name, 'sha256': sha})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_primary24_pair_frozen_matcher')
    require(matcher.ROOT == matcher.assets.ROOT == matcher.fixtures.native.ROOT == root, 'Local imports')
    matcher.assets.original_files.cache_clear()
    for name, sha in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
                      ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH), ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': sha})
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH
            and report['sourceClosure'] == [{'path': n, 'sha256': s} for n, s in pins.items()], 'Frozen generator/source closure')
    rom, files = matcher.assets.original_files()
    require(report['romSha256'] == matcher.assets.ROM_HASH and len(report['units']) == 2, 'Original ROM/two-unit population')
    units = {}
    for item, kind in zip(report['units'], ('enable', 'clear')):
        native_unit = matcher.fixtures.UNITS[kind]
        data = matcher.assets.load(root / 'extract/files' / native_unit['asset'])
        raw, interval = (root / data['asset']).read_bytes(), files[native_unit['asset']]
        require(item['kind'] == kind and raw == rom[interval[0]:interval[1]] and item['romFileRange'] == list(interval)
                and item['archiveSha256'] == data['assetSha256'] and item['scriptSha256'] == data['scriptSha256']
                and item['codeSha256'] == digest(data['code']), 'Current qualified image/ROM interval')
        name = 'enable_primary_24_from_argument' if kind == 'enable' else 'clear_primary_24_from_argument'
        require(item['source'] == 'src/scripts/20261030/batch10/' + name + '.c', 'Actual ordinary source identity')
        profile = json.loads((matcher.SOURCE / (name + '.bindings.json')).read_text())
        require(item['boundariesAndStorage'] == matcher.boundary(data, native_unit, profile), 'Actual assignments dominate every source read and outside references audited')
        build = item['sourceOnlyBuild']
        require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False, 'Source-only build')
        expected_directory = root / 'work/script-source/20261030/batch10/primary24-pair' / kind / 'source-only'
        require(build['cwd'] == str(expected_directory) and build['command'] == [sys.executable,
                'scr_c_compiler_20261030_v8.py', '--source', name + '.c', '--base', hex(native_unit['base']),
                '--bindings', name + '.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json'],
                'Actual source-only command and directory')
        inputs = {Path(x['path']).name: checked(root, x) for x in build['inputs']}
        expected = {'scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py', 'scr_c_compiler_20261030_v6.py',
                    'scr_c_compiler_20261030_v8.py', name + '.c', 'scr_formal_decision.h', name + '.bindings.json'}
        require(set(inputs) == expected and len(build['inputs']) == 7, 'Complete source-only closure')
        for filename, p in inputs.items():
            origin = filename if filename.endswith('.py') else 'src/scripts/20261030/batch10/' + filename
            require(digest(p.read_bytes()) == pins[origin], 'Copied compiler/C/header/profile identity')
        body = checked(root, build['emittedBody']).read_bytes()
        evidence = json.loads(checked(root, build['compilerReport']).read_text())
        require(evidence == build['compilerEvidence'] and body == data['code'][native_unit['base']:native_unit['end']], 'Complete source product')
        stage = root / 'work/script-source/20261030/batch10/validator'
        stage.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=kind + '-', dir=stage) as temporary:
            directory = Path(temporary)
            for filename, p in inputs.items():
                shutil.copyfile(p, directory / filename)
            subprocess.run(build['command'], cwd=directory, capture_output=True, text=True, timeout=30, check=True)
            require((directory / 'generated.scrfunc').read_bytes() == body and json.loads((directory / 'build.json').read_text()) == evidence,
                    'Fresh isolated source-only rebuild and compiler evidence')
        require(checked(root, build['rebuiltImage']).read_bytes() == data['script']
                and item['matchedRange'] == {'startPc': native_unit['base'], 'endExclusivePc': native_unit['end'],
                    'bytes': len(body), 'sha256': digest(body)}, 'Current rebuilt image/full range')
        for control in item['compilerControls']['rejectedSourceProfiles']:
            source = checked(root, control['source'])
            require((source.parent / 'scr_formal_decision.h').read_bytes() == (matcher.SOURCE / 'scr_formal_decision.h').read_bytes(), 'Negative include closure')
            try:
                matcher.compiler.compile_source(source, native_unit['base'], control['bindings'])
            except ValueError as error:
                require(str(error) == control['error'] and control['rejectedBeforeOutput'] is True, 'Current source/profile rejection')
            else:
                raise ValueError('Negative formal decision compiles')
        require(len(item['compilerControls']['rejectedSourceProfiles']) == (7 if kind == 'enable' else 10), 'Definite-assignment negative controls')
        native_proof(item, native_unit, data)
        require(item['sourceDefinitionCount'] == item['completeFunctionInstances'] == 1 and item['scaffoldingSourceCredit'] == 0
                and item['prefixOuterEntryReturnCredit'] == item['prefixAdditionalSourceCredit'] == 0, 'No excess source or outer return credit')
        key = digest(data['code']), native_unit['base']
        units[key] = {'codeSha256': key[0], 'scriptSha256': data['scriptSha256'], 'asset': data['asset'],
            'startPc': key[1], 'endExclusivePc': native_unit['end'], 'bytes': len(body), 'sha256': digest(body),
            'mode': 'SCR', 'vmHostProcessor': 'ARM9', 'entryAliases': [102], 'source': item['source'],
            'sourceSha256': evidence['sourceSha256'], 'sourceDefinitionCount': 1, 'substantiveDecisionLogicBytes': len(body),
            'pairedNativeReturningCalls': item['pairedNativeReturningCalls'], 'pairedCompleteOwnEntryExecutions': item['pairedCompleteOwnEntryExecutions'],
            'prefixOuterEntryReturnCredit': 0, 'wholeImageReconstructed': False}
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == len(units) == 2
            and report['qualifiedScriptRangeBytes'] == sum(u['bytes'] for u in units.values()) == 1016, 'Qualified source population')
    require(report['pairedNativeReturningCalls'] == sum(u['pairedNativeReturningCalls'] for u in units.values())
            and report['pairedCompleteOwnEntryExecutions'] == sum(u['pairedCompleteOwnEntryExecutions'] for u in units.values()), 'Accurate complete-entry versus helper totals')
    require(report['pairedPrefixNativeReturningCalls'] == sum(u['prefixNativeReturningCalls'] for u in report['units']), 'Accurate separate prefix total')
    require(report['nativeExecutableByteCredit'] == report['completeImagesRecovered'] == report['nativeFunctionStubs'] == 0
            and report['postFaultStateUsedForProof'] is False and report['wholeRomSourceMatch'] is False
            and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'Evidence scope')
    return units


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(u['bytes'] for u in units.values())}))
