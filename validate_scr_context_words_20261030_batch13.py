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
assert hashlib.sha256(SHARED.read_bytes()).hexdigest() == 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020'
SPEC = importlib.util.spec_from_file_location('_context_words_shared', SHARED)
shared = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_context_words_20261030_batch13.py'
MATCHER_HASH = '347259ba0f56beff89b083d020e233a9acc0dbe44f4d82629573489b3e627b44'
REPORT = 'evidence/matches/scripts-20261030-context-words.json'


def initial_state(matcher, seed, numeric, flags, counter):
    native = matcher.fixtures.native
    state = bytearray(random.Random(seed).randbytes(0x7040))
    struct.pack_into('<I', state, 4, counter)
    for index, value in zip((0, 3, 20), numeric):
        state[native.NUMERIC + index - native.PERSIST] = value
    for bit, index in enumerate((209, 210, 212, 211)):
        native.bit_set(state, native.PRIMARY, index, bool(flags & (1 << bit)))
    return bytes(state)


def invocation(matcher, part, observations, registers, before_words, numeric, flags, counter, persistent, instructions):
    native, base, end = matcher.fixtures.native, 43972, 45252
    conditions = {44072: numeric[0] == 2, 44164: numeric[1] <= 6, 44368: numeric[0] == 3,
        44528: not flags & 1, 44688: not flags & 2, 44848: not flags & 4,
        45008: not flags & 8, 45168: numeric[2] <= 28}
    words, args, pc = list(before_words), [0, 0], base
    actions, branches, reads, stores, trace = [], [], [], [], []
    require(part['registerFileBeforeHex'] == bytes(registers).hex() and part['contextWordsBefore'] == words,
        'Complete register-file/context-word carry')
    for observation in observations:
        row = instructions[pc]
        opcode, raw, size = row['opcode'], row['argumentsRaw'], row['bytes']
        following = pc + size
        if opcode == 1036:
            following = raw[1]
        elif opcode == 1038:
            taken = not conditions[pc]
            following = raw[1] if taken else following
            branches.append({'pc': pc, 'takenToEncodedTarget': taken})
        elif opcode == 1045:
            destination_mode, destination = raw[1], int(matcher.assets.f32(raw[2]))
            if destination_mode == 1:
                require(raw[3] == 2 and destination in (0, 1), 'Typed immediate API arguments')
                args[destination] = int(matcher.assets.f32(raw[4]))
            else:
                require(destination_mode == 0 and destination in (67, 68) and raw[3:] == [1, 0], 'Typed local getter captures')
                struct.pack_into('<I', registers, destination * 4, matcher.fixtures.fword(args[0]))
        elif opcode in (39, 41):
            index = args[0]
            value = numeric[(0, 3, 20).index(index)] if opcode == 39 else int(bool(flags & (1 << (209, 210, 212, 211).index(index))))
            reads.append({'pc': pc, 'api': 'get_numeric_state' if opcode == 39 else 'get_primary_flag', 'index': index, 'value': value})
            args[0] = value
        elif opcode == 162:
            words = [counter] * 16
            stores += [{'address': hex(0x021C51D0 + index * 4), 'bytes': 4, 'value': counter} for index in range(16)]
            actions.append({'pc': pc, 'api': 'reset_context_words', 'rawCounterWord': counter})
        elif opcode == 161:
            index, value = args
            words[index] = value
            stores.append({'address': hex(0x021C51D0 + index * 4), 'bytes': 4, 'value': value})
            actions.append({'pc': pc, 'api': 'set_context_word', 'index': index, 'value': value})
        elif opcode == 1026:
            following = pc
        else:
            require(opcode in (1024, 1039, 1044), 'Supported context-word record class')
        require(observation['entry'] == ('0x204c5a0' if opcode >= 1024 else '0x205a65c')
            and observation['resultWord'] == 1 and observation['persistentSha256'] == digest(persistent),
            'Actual native result/persistent invariant per record')
        trace.append({'pc': pc, 'opcode': opcode, 'nextPc': following})
        pc = following
    require(trace[-1]['pc'] == end - 4 and trace[-1]['opcode'] == 1026
        and part['completeEntryReturned'] is True and part['privateReturnPc'] == end - 4,
        'Complete private-return termination')
    require(part['trace'] == trace and part['actions'] == actions and part['branches'] == branches
        and part['getterReads'] == reads, 'Every supported branch/read/API action')
    require(part['orderedContextWordStores'] == stores and part['contextWordsAfter'] == words
        and words == matcher.fixtures.modeled_words(counter, numeric, flags), 'Ordered reset/set word effects')
    require(part['persistentInvariantSha256'] == digest(persistent) and part['registerFileAfterSha256'] == digest(registers)
        and part['allOtherSlotsAndWordGuardsPreserved'] is True, 'Full persistent/register/neighbor preservation')
    return words


def native_proof(matcher, report):
    proof = report['differential']
    data = matcher.assets.load(ROOT / 'extract/files/world.e')
    instructions = {row['pc']: row for row in data['instructions'] if 43972 <= row['pc'] < 45252}
    require(len(proof['cases']) == proof['freshMachines'] == 320 and proof['providerCount'] == 0
        and proof['scriptStepCap'] == 200 and proof['nativeInstructionCap'] == 20000
        and proof['nativeTimeoutMicroseconds'] == 1000000 and proof['serializedCompleteCallsOnly'] is True
        and proof['naturalSceneOrRenewabilityMeaningProven'] is False, 'Fresh bounded native population/scope')
    calls, records, branches = 0, set(), {}
    for index, case in enumerate(proof['cases']):
        thread, flags, numeric, seed = index // 80, index % 80 // 5, matcher.fixtures.NUMERIC_CASES[index % 5], 2026103019000 + index
        counter = (0, 1, 10800, 0xFFFFFFFF)[thread]
        require((case['thread'], case['flags'], tuple(case['numeric']), case['seed'], case['rawCounterWord']) ==
            (thread, flags, numeric, seed, counter) and case['providerCount'] == 0, 'Typed input/thread/counter population')
        persistent = initial_state(matcher, seed, numeric, flags, counter)
        initial = random.Random(seed ^ 0x161).randbytes(72)
        require(case['originalContextWordsBeforeHex'] == initial.hex(), 'Independently seeded word guards')
        words = list(struct.unpack('<16I', initial[4:68]))
        observations = case['observations']
        shared.observations(observations)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([row['entry'] for row in observations[:len(startup)]] == startup, 'Natural native init/start/forks')
        registers = bytearray.fromhex(case['first']['registerFileBeforeHex'])
        require(len(registers) == 1024, 'All256 VM words present')
        cursor = len(startup)
        for ordinal, name in enumerate(('first', 'second')):
            if ordinal:
                require(observations[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0'), 'Natural serialized reentry')
                cursor += 1
            part = case[name]
            end = cursor + len(part['trace'])
            words = invocation(matcher, part, observations[cursor:end], registers, words, numeric, flags, counter, persistent, instructions)
            cursor = end
            records.update(row['pc'] for row in part['trace'])
            for branch in part['branches']:
                branches.setdefault(str(branch['pc']), set()).add(branch['takenToEncodedTarget'])
        require(cursor == len(observations) == case['actualReturningCalls'], 'Per-case actual-return count')
        calls += cursor
    require(all(values == {False, True} for values in branches.values()) and proof['branchCoverage'] ==
        {pc: sorted(values) for pc, values in branches.items()}, 'All own branch outcomes')
    require(proof['executedOwnRecordPcs'] == sorted(records) == report['boundariesAndStorage']['reachableOwnRecordPcs'],
        'All own complete records executed')
    require(proof['actualReturningCalls'] == calls and report['pairedNativeReturningCalls'] == calls * 2
        and proof['completeEntryExecutions'] == 640 and report['pairedCompleteOwnEntryExecutions'] == 1280,
        'Separate native/complete-entry return counts')


def compiler_controls(matcher, report):
    proof = report['compilerControls']
    require(len(proof['rejectedSourceProfiles']) == 10 and proof['controlSourceCredit'] == 0
        and proof['arbitraryContextFloatOrderingSupportClaimed'] is False, 'Negative source/type/domain scope')
    for row in proof['rejectedSourceProfiles']:
        source = checked(ROOT, row['source'])
        require((source.parent / 'scr_context_words.h').read_bytes() == (matcher.SOURCE / 'scr_context_words.h').read_bytes(), 'Control ABI closure')
        try:
            matcher.compiler.compile_source(source, 43972, row['bindings'])
        except ValueError as error:
            require(str(error) == row['error'] and row['rejectedBeforeOutput'] is True, 'Actual source rejection')
        else:
            raise ValueError('Unsupported context-word source compiled')
    source = checked(ROOT, proof['byteRelationSource'])
    body, compiled = matcher.compiler.compile_source(source, 0, {'locals': {'value': 96}, 'globals': {}})
    require(json.loads(json.dumps(compiled)) == proof['byteRelationBuild'], 'Fresh synthetic <= source build')
    require(len(proof['all256ByteRelationCases']) == 256, 'Exhaustive byte relation domain')
    for value, case in enumerate(proof['all256ByteRelationCases']):
        expected = [0xA5A5A5A5] * 16
        if value <= 6:
            expected[2] = 1
        if value <= 28:
            expected[3] = 1
        require(case['numeric3'] == value and case['expectedContextWords'] == expected and case['completeControlReturned'] is True
            and case['sourceCredit'] == 0 and case['trace'][-1]['opcode'] == 1026, 'All256 true <= and returning controls')
        shared.observations(case['observations'])
        require(case['actualReturningCalls'] == len(case['observations']) == len(case['trace']) + 2, 'Separate synthetic return counts')
    require(sum(case['actualReturningCalls'] for case in proof['all256ByteRelationCases']) == proof['byteRelationActualReturningCalls'] ==
        report['separateByteControlNativeReturns'], 'Separate byte control totals')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Local pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(node.value) for node in ast.parse(path.read_text()).body if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'PINS' for target in node.targets))
    for name, pin in pins.items():
        checked(root, {'path': name, 'sha256': pin})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_context_words_frozen_matcher')
    for name, pin in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
            ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH),
            ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': pin})
    matcher.assets.original_files.cache_clear()
    data = matcher.assets.load(root / 'extract/files/world.e')
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['evidenceClass'] == 'ordinary-C-complete-numeric-primary-context-word-SCR-source-match',
        'Ordinary complete context-word source evidence class')
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH and report['sourceClosure'] ==
        [{'path': name, 'sha256': pin} for name, pin in pins.items()], 'Frozen source/generator closure')
    rom, files = matcher.assets.original_files()
    interval = files['world.e']
    require((root / data['asset']).read_bytes() == rom[interval[0]:interval[1]] and report['romSha256'] == matcher.assets.ROM_HASH
        and report['romFileRange'] == list(interval) and report['archiveSha256'] == data['assetSha256']
        and report['scriptSha256'] == data['scriptSha256'] and report['codeSha256'] == digest(data['code']), 'Current original ROM/image identity')
    require(report['boundariesAndStorage'] == matcher.boundary(data) and report['nativeContracts'] == matcher.native_contracts(),
        'Current private/direct/slot bounds and native ABI')
    build = report['sourceOnlyBuild']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False and build['cwd'] ==
        str(root / 'work/script-source/20261030/batch13/context-words/source-only') and build['command'] ==
        [sys.executable, 'scr_c_compiler_20261030_v11.py', '--source', 'refresh_context_words.c', '--base', hex(43972),
        '--bindings', 'context.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json'], 'Actual source-only command/directory')
    inputs = {Path(row['path']).name: checked(root, row) for row in build['inputs']}
    require(len(inputs) == len(build['inputs']) == 7, 'Complete source-only closure')
    for name, path in inputs.items():
        origin = name if name.endswith('.py') else 'src/scripts/20261030/batch13/' + name
        require(digest(path.read_bytes()) == pins[origin], 'Copied source-only input identity')
    body = checked(root, build['emittedBody']).read_bytes()
    compiled = json.loads(checked(root, build['compilerReport']).read_text())
    require(body == data['code'][43972:45252] and compiled == build['compilerEvidence'] and compiled['generalCCompilerClaimed'] is False,
        'Complete1280B ordinary source product')
    stage = root / 'work/script-source/20261030/batch13/validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for name, path in inputs.items():
            shutil.copyfile(path, directory / name)
        subprocess.run(build['command'], cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        require((directory / 'generated.scrfunc').read_bytes() == body and json.loads((directory / 'build.json').read_text()) == compiled,
            'Fresh isolated source-only rebuild')
    require(report['matchedRange'] == {'startPc': 43972, 'endExclusivePc': 45252, 'bytes': 1280, 'sha256': digest(body)}
        and checked(root, build['rebuiltImage']).read_bytes() == data['script'], 'Complete current source range/image')
    compiler_controls(matcher, report)
    native_proof(matcher, report)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1 and report['qualifiedScriptRangeBytes'] == 1280
        and report['originalScaffoldingBytes'] == len(data['script']) - 1280, 'One complete source unit scope')
    require(all(report[key] == 0 for key in ('scaffoldingSourceCredit', 'completeImagesRecovered', 'nativeExecutableByteCredit', 'nativeFunctionStubs'))
        and report['wholeRomSourceMatch'] is False and report['postFaultStateUsedForProof'] is False
        and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'No excess credit or post-fault state')
    return {(digest(data['code']), 43972): {'codeSha256': digest(data['code']), 'scriptSha256': data['scriptSha256'], 'asset': data['asset'],
        'startPc': 43972, 'endExclusivePc': 45252, 'bytes': 1280, 'sha256': digest(body), 'entryAliases': [272],
        'mode': 'SCR', 'vmHostProcessor': 'ARM9', 'source': 'src/scripts/20261030/batch13/refresh_context_words.c',
        'sourceSha256': compiled['sourceSha256'], 'sourceDefinitionCount': 1,
        'pairedCompleteOwnEntryExecutions': report['pairedCompleteOwnEntryExecutions'],
        'pairedNativeReturningCalls': report['pairedNativeReturningCalls'], 'wholeImageReconstructed': False}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(row['bytes'] for row in units.values())}))
