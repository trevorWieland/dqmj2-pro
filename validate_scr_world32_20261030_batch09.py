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
spec = importlib.util.spec_from_file_location('_world32_shared', SHARED)
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_world32_20261030_batch09.py'
MATCHER_HASH = '1c890c982e04eccafa7bfd7e4bd8c1cd88d10d1d2fe61156c7581eab12b17966'
REPORT = 'evidence/matches/scripts-20261030-world32.json'
BASE, END = 60232, 63972
PERSIST, NUMERIC, PRIMARY = 0x021B9EB4, 0x021C0DC8, 0x021C0E20
CLEAR_FLAGS = [2, 62, 61, 289, 318, 320, 322, 324, 328, 319, 331, 332, 330, 325, 321, 323, 329, 333,
               363, 338, 351, 352, 346, 347, 348, 349, *range(500, 510), *range(245, 252), 259,
               *range(252, 259), *range(273, 281), 271]
CALLS = [(63860, 1056), (63872, 64268), (63884, 43972), (63896, 50684),
         (63932, 52244), (63944, 59052), (63956, 59076)]


def word(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def floating(value):
    return struct.unpack('<f', struct.pack('<I', value))[0]


def set_bit(state, index, value):
    offset, mask = PRIMARY + index // 8 - PERSIST, 1 << (index & 7)
    state[offset] = state[offset] | mask if value else state[offset] & ~mask


def owned_effects(part, before, registers, input_word, rng, decoded, observations):
    state, args, actions, stores = bytearray(before), {0: input_word}, [], []
    sampled, predicate = None, None
    own_prefix = []
    for step in part['trace']:
        if step['pc'] == CALLS[0][0]:
            break
        own_prefix.append(step)
    for step, observation in zip(own_prefix, observations):
        row = decoded[step['pc']]
        op, x = row['opcode'], row['argumentsRaw']
        if op == 1045:
            mode, destination, source_mode, source = x[1:]
            if source_mode == 2:
                value = source
            else:
                slot = int(floating(source))
                require(source_mode in (0, 1), 'Direct caller operand source')
                value = struct.unpack_from('<I', registers, slot * 4)[0] if source_mode == 0 else args[slot]
            index = int(floating(destination))
            if mode == 0:
                struct.pack_into('<I', registers, index * 4, value)
            else:
                require(mode == 1, 'Direct caller argument destination')
                args[index] = value
        elif op in (40, 42):
            index, value = int(floating(args[0])), int(floating(args[1]))
            numeric = op == 40
            previous = state[NUMERIC + index - PERSIST] if numeric else int(bool(state[PRIMARY + index // 8 - PERSIST] & (1 << (index & 7))))
            if numeric:
                state[NUMERIC + index - PERSIST] = value
                stores.append({'address': hex(NUMERIC + index), 'bytes': 1, 'value': value})
            else:
                set_bit(state, index, value)
                address = PRIMARY + (index >> 5) * 4
                stores.append({'address': hex(address), 'bytes': 4, 'value': struct.unpack_from('<I', state, address - PERSIST)[0]})
            actions.append({'pc': step['pc'], 'api': 'numeric' if numeric else 'primary', 'index': index, 'value': value})
            args[0] = word(previous)
        elif op == 43:
            require(floating(args[0]) == 0, 'Qualified zero counter input')
            struct.pack_into('<II', state, 0x1C, 0, 0)
            stores += [{'address': hex(PERSIST + 0x20), 'bytes': 4, 'value': 0}, {'address': hex(PERSIST + 0x1C), 'bytes': 4, 'value': 0}]
            actions.append({'pc': step['pc'], 'api': 'reset-counter', 'value': 0})
        elif op == 36:
            require(floating(args[0]) == 7, 'Positive random bound')
            following = (rng * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
            sampled = (following >> 16) % 7
            actions.append({'pc': step['pc'], 'api': 'sample-positive-random', 'bound': 7,
                            'rngBefore': rng, 'rngAfter': following, 'value': sampled})
            args[0] = word(sampled)
        elif op == 48:
            count = struct.unpack_from('<I', state, 4)[0]
            predicate = int(count >= 10800)
            actions.append({'pc': step['pc'], 'api': 'runtime-counter-threshold', 'counter': count, 'value': predicate})
            args[0] = word(predicate)
        else:
            require(op == 1036, 'Caller prefix contains only qualified straight-line operations')
        require(observation['persistentSha256'] == digest(state), 'Independent full own persistent state per step')
    require(part['directActions'] == actions and part['ownPersistentStores'] == stores, 'Independent own actions/word-store order')
    require([(a['index'], a['value']) for a in actions if a['api'] == 'primary'] == [(i, 0) for i in CLEAR_FLAGS] + [(145, predicate)],
            'All60 clear flags and threshold flag')
    require(part['registerFileAtFirstCalleeSha256'] == digest(registers), 'Complete own register file before inherited callees')
    require(part['finalCallerLocalWords'] == [input_word, word(sampled), word(predicate)], 'Typed formal/RNG/bool results')
    require(part['ownWholeRegisterFileChecks'] == 204 and part['threeCallerLocalsPreservedByCallees'] is True,
            'Every own record checks whole register file and inherited callees preserve caller slots')
    return sampled, predicate


def invocation(part, before, before_registers, input_word, rng, decoded, observations):
    require(bytes.fromhex(part['persistentBeforeHex']) == before
            and bytes.fromhex(part['registerFileBeforeHex']) == before_registers, 'Exact invocation state chain')
    registers = bytearray(before_registers)
    sampled, predicate = owned_effects(part, before, registers, input_word, rng, decoded, observations)
    stack, expected_pc, own_calls = [], BASE, []
    for step in part['trace']:
        pc, op = step['pc'], step['opcode']
        require(pc == expected_pc and pc in decoded and decoded[pc]['opcode'] == op
                and step['depthBefore'] == len(stack), 'Exact current record/ABI depth')
        row, next_pc = decoded[pc], step['nextPc']
        if op == 1033:
            stack.append(pc + row['bytes'])
            require(next_pc == row['argumentsRaw'][1], 'Qualified direct CALL target')
            if BASE <= pc < END:
                own_calls.append((pc, next_pc))
        elif op == 1026:
            require(next_pc == (stack.pop() if stack else pc), 'Real private or inherited RET continuation')
        elif op == 1036:
            require(next_pc == row['argumentsRaw'][1], 'Direct jump target')
        elif op == 1038:
            require(next_pc in (pc + row['bytes'], row['argumentsRaw'][1]), 'Original callee conditional boundary')
        else:
            require(next_pc == pc + row['bytes'], 'Decoded instruction extent')
        require(step['depthAfter'] == len(stack), 'Actual balanced call depth')
        expected_pc = next_pc
    require(part['trace'][-1]['pc'] == END - 4 and part['trace'][-1]['opcode'] == 1026 and not stack
            and part['entry32Returned'] is True, 'Whole caller return, no boundary stop')
    require(own_calls == CALLS and [(a['pc'], a['targetPc']) for a in part['directScriptCalls']] == CALLS
            and part['directScriptCalls'][4]['argument0Word'] == input_word, 'Ordered seven calls/float formal handoff')
    after, final_file = bytes.fromhex(part['persistentAfterHex']), bytes.fromhex(part['registerFileAfterHex'])
    require(len(after) == 0x7040 and len(final_file) == 1024 and digest(after) == part['persistentAfterSha256']
            and observations[-1]['persistentSha256'] == digest(after), 'Complete return state')
    require(list(struct.unpack_from('<3I', final_file, 100 * 4)) == [input_word, word(sampled), word(predicate)],
            'Raw final caller slots retained')
    return after, final_file


def native_proof(report, data):
    proof = report['differential']
    require(proof['nativeInstructionCap'] == 20000 and proof['nativeTimeoutMicroseconds'] == 1000000
            and proof['scriptStepBound'] == 3000 and proof['serializedCompleteCallsOnly'] is True
            and proof['naturalSceneOrRenewabilityMeaningProven'] is False and proof['all4Threads'] is True, 'Execution scope/bounds')
    words, counts, rngs = [0, 0x80000000, 0x3F800000, 0x7FC00001], [0, 10799, 10800, 0xFFFFFFFF], [0, 1, 0xFFFFFFFF, 0x12345678]
    require(len(proof['cases']) == 16, 'All4threads/4formal inputs/threshold boundaries')
    decoded, calls, owned = {r['pc']: r for r in data['instructions']}, 0, set()
    for index, case in enumerate(proof['cases']):
        phase, thread = divmod(index, 4)
        seed, input_word, rng, pattern, gate = 2026103009500 + index, words[phase], rngs[(phase + thread) % 4], bool(thread & 1), bool((phase + thread) & 1)
        require({key: case[key] for key in ('seed', 'thread', 'inputWord', 'thresholdCounter', 'rngSeed', 'initialClearFlags', 'numeric20Gate', 'numeric0', 'numeric1')} ==
                {'seed': seed, 'thread': thread, 'inputWord': input_word, 'thresholdCounter': counts[phase], 'rngSeed': rng,
                 'initialClearFlags': pattern, 'numeric20Gate': gate, 'numeric0': 4, 'numeric1': 0}, 'Scenario identity')
        state = bytearray(random.Random(seed).randbytes(0x7040))
        state[NUMERIC - PERSIST:NUMERIC + 2 - PERSIST] = bytes((4, 0))
        state[NUMERIC + 20 - PERSIST], state[NUMERIC + 28 - PERSIST] = 28 if gate else 27, 5
        set_bit(state, 218, True)
        for flag in CLEAR_FLAGS:
            set_bit(state, flag, pattern)
        struct.pack_into('<I', state, 4, counts[phase])
        registers = random.Random(seed ^ 0x947).randbytes(1024)
        observed = case['observations']
        shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([a['entry'] for a in observed[:len(startup)]] == startup
                and all(a['persistentSha256'] == digest(state) for a in observed[:len(startup)]), 'Fresh native init/start/fork')
        cursor = len(startup)
        for ordinal, key in enumerate(('first', 'second')):
            if ordinal:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0')
                        and observed[cursor]['persistentSha256'] == digest(state), 'Serialized native reentry')
                cursor += 1
                rng = case['first']['rngAfter']
            part = case[key]
            end = cursor + len(part['trace'])
            current = observed[cursor:end]
            require([a['entry'] for a in current] == ['0x205a65c' if s['opcode'] < 1024 else '0x204c5a0' for s in part['trace']]
                    and all(a['resultWord'] == 1 for a in current), 'Every true native dispatch return')
            state, registers = invocation(part, bytes(state), registers, input_word, rng, decoded, current)
            owned.update(s['pc'] for s in part['trace'] if BASE <= s['pc'] < END)
            cursor = end
        require(cursor == len(observed) == case['actualReturningCalls'], 'Exact returning population')
        calls += cursor
    require(owned == {pc for pc in decoded if BASE <= pc < END} and report['executedOwnRecordPcs'] == sorted(owned)
            and report['allOwnRecordsExecuted'] is True, 'Every own instruction executed')
    require(calls == proof['actualReturningCalls'] == report['actualReturningCallsPerImplementation'] == 26038
            and report['actualReturningCallsTotal'] == 52076
            and proof['freshMachines'] == report['freshMachinesPerImplementation'] == 16, 'Paired whole-entry proof totals')


def source_builds(root, matcher, report, data, pins):
    expected = [('caller', 60232, 63972, 3740), ('linked-entry34', 64268, 65620, 0), ('linked-entry20', 59052, 59068, 0)]
    require(len(report['sourceOnlyBuilds']) == 3, 'Actual caller plus two source-linked products')
    for record, (name, start, end, credit) in zip(report['sourceOnlyBuilds'], expected):
        require((record['startPc'], record['endExclusivePc'], record['bytes'], record['sourceCredit']) == (start, end, end - start, credit), 'Linked unit scope')
        build = record['build']
        require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False, 'Source-only linked compilation')
        inputs = {Path(item['path']).name: checked(root, item) for item in build['inputs']}
        for filename, path in inputs.items():
            require(digest(path.read_bytes()) in pins.values(), 'Every copied input from frozen closure')
        body = checked(root, build['emittedBody']).read_bytes()
        evidence = json.loads(checked(root, build['compilerReport']).read_text())
        require(evidence == build['compilerEvidence'] and body == data['code'][start:end], 'Fresh actual source-linked body')
        original_directory = root / 'work/script-source/20261030/batch09/world32' / name
        command = build['command']
        require(build['cwd'] == str(original_directory) and command[0] == sys.executable
                and command[command.index('--source') + 1] in inputs and command[command.index('--base') + 1] == hex(start), 'Actual command/CWD')
        require('--output' in command and '--report' in command and all((original_directory / key).resolve() == value.resolve() for key, value in inputs.items()),
                'Actual source-only directory products')
        stage = root / 'work/script-source/20261030/batch09/validator'
        stage.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=name + '-', dir=stage) as temporary:
            directory = Path(temporary)
            for filename, path in inputs.items():
                shutil.copyfile(path, directory / filename)
            subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
            require((directory / 'generated.scrfunc').read_bytes() == body, 'New source-only linked emission')
            fresh = json.loads((directory / 'build.json').read_text())
            for key in ('sourcePath', 'includePath', 'compilerPath'):
                if key in evidence:
                    require(Path(evidence[key]).parent == original_directory and Path(fresh[key]).parent == directory
                            and Path(fresh[key]).name == Path(evidence[key]).name, 'Relocatable source evidence path')
                    fresh[key] = evidence[key]
            require(fresh == evidence, 'Rebuilt compiler evidence, semantic hashes unchanged')
    require(checked(root, report['rebuiltDecodedImage']).read_bytes() == data['script'], 'Actually executed source-linked image')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Local root/pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(n.value) for n in ast.parse(path.read_text()).body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in n.targets))
    for name, sha in pins.items():
        checked(root, {'path': name, 'sha256': sha})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_world32_frozen_matcher')
    require(matcher.ROOT == matcher.assets.ROOT == matcher.fixtures.native.ROOT == root, 'Local imports')
    matcher.assets.original_files.cache_clear()
    for name, sha in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
                      ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH), ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': sha})
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH
            and report['sourceClosure'] == [{'path': n, 'sha256': s} for n, s in pins.items()], 'Frozen source/generator closure')
    data = matcher.assets.load(root / 'extract/files/world.e')
    rom, files = matcher.assets.original_files()
    raw, interval = (root / data['asset']).read_bytes(), files['world.e']
    require(raw == rom[interval[0]:interval[1]] and report['romSha256'] == matcher.assets.ROM_HASH and report['romFileRange'] == list(interval), 'Original ROM/interval')
    require(report['archiveSha256'] == data['assetSha256'] and report['scriptSha256'] == data['scriptSha256']
            and report['codeSha256'] == digest(data['code']), 'Current archive/decoded source identity')
    for index in range(matcher.assets.u32(raw, 4)):
        offset, size = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
        require(matcher.assets.ash(raw[offset:offset + size]) == data['script'], 'Archive aliases')
    profile = json.loads((matcher.SOURCE / 'reset.locals.json').read_text())
    links = json.loads((matcher.SOURCE / 'reset.links.json').read_text())
    require(report['boundariesAndLinks'] == matcher.boundary(data, profile, links), 'Complete bounds and private-slot references')
    require(report['namedNativeApiContracts'] == matcher.native_contracts(), 'Measured native wrapper identities')
    source_builds(root, matcher, report, data, pins)
    require(report['matchedRange'] == {'startPc': BASE, 'endExclusivePc': END, 'bytes': 3740, 'sha256': digest(data['code'][BASE:END])}, 'Full3740B source body')
    controls = report['compilerControls']
    require(len(controls['rejectedSourceProfilesLinks']) == 13 and controls['wrongAlignedBindingChangesBytes'] is True
            and controls['wrongAlignedBindingQualifiedAgainstCurrentImage'] is False and controls['negativeControlSourceCredit'] == 0, 'Source/link controls')
    wrong = json.loads(json.dumps(links))
    wrong['reset_shared_flags']['entryPc'] += 4
    wrong_body, unused = matcher.compiler.compile_source(matcher.SOURCE / 'reset_world_flags.c', BASE, profile, wrong)
    require(wrong_body != data['code'][BASE:END], 'Measured different emitted bytes for wrong aligned binding')
    try:
        matcher.boundary(data, profile, wrong)
    except AssertionError:
        pass
    else:
        raise ValueError('Wrong aligned target qualified against the current image')
    for item in controls['rejectedSourceProfilesLinks']:
        source = checked(root, item['source'])
        require((source.parent / 'scr_reset_caller.h').read_bytes() == (matcher.SOURCE / 'scr_reset_caller.h').read_bytes(), 'Control header closure')
        try:
            matcher.compiler.compile_source(source, BASE, item['profile'], item['links'])
        except (ValueError, TypeError) as error:
            require(str(error) == item['error'] and item['rejectedBeforeOutput'] is True, 'Current rejection reason')
        else:
            raise ValueError('Negative reset caller now compiles')
    native_proof(report, data)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1 and report['qualifiedScriptRangeBytes'] == 3740
            and report['reusedSourceLinkedCalleeBytes'] == 1368 and report['qualifiedOriginalCalleeCount'] == 5, 'Source unit scope')
    for key in ('reusedSourceLinkedCalleeNewCredit', 'qualifiedOriginalCalleeSourceCredit', 'scaffoldingSourceCredit', 'completeImagesRecovered', 'nativeExecutableByteCredit', 'nativeFunctionStubs'):
        require(report[key] == 0, 'No additional credit: ' + key)
    require(report['wholeRomSourceMatch'] is False and report['postFaultStateUsedForProof'] is False
            and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'Native comparison scope')
    key = digest(data['code']), BASE
    return {key: {'codeSha256': key[0], 'scriptSha256': data['scriptSha256'], 'asset': data['asset'], 'startPc': BASE,
        'endExclusivePc': END, 'bytes': 3740, 'sha256': digest(data['code'][BASE:END]), 'mode': 'SCR', 'vmHostProcessor': 'ARM9',
        'entryAliases': [32], 'source': 'src/scripts/20261030/batch09/reset_world_flags.c', 'sourceSha256': pins['src/scripts/20261030/batch09/reset_world_flags.c'],
        'sourceDefinitionCount': 1, 'substantiveResetLogicBytes': 3740, 'actualReturningCallsTotal': 52076,
        'sourceLinkedCalleeReuseBytes': 1368, 'sourceLinkedCalleeNewCredit': 0, 'originalCalleeSourceCredit': 0, 'wholeImageReconstructed': False}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(u['bytes'] for u in units.values())}))
