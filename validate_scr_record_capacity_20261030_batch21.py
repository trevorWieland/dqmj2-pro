import ast
import hashlib
import importlib.util
import json
import math
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
spec = importlib.util.spec_from_file_location('_record_capacity_shared', SHARED)
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_record_capacity_20261030_batch21.py'
MATCHER_HASH = 'e046f4aa2eb4d33f0990725b8c92f11f8ecc250b4be119391eab27c84aa687de'
REPORT = 'evidence/matches/scripts-20261030-record-capacity.json'


def fword(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def number(word):
    return struct.unpack('<f', struct.pack('<I', word))[0]


def native_proof(report, module, data):
    proof, native = report['differential'], module.fixtures.native
    require(proof['freshMachines'] == len(proof['cases']) == 104 and proof['providerCount'] == 0 and proof['nativeInstructionCap'] == 20000
        and proof['nativeTimeoutMicroseconds'] == 1000000 and proof['scriptStepCap'] == 40 and proof['allOriginalCounterCallsRetained'] is True
        and proof['serializedReentryChecked'] is True and proof['nativeUIDWordCountOnly'] is True
        and proof['fullRecordValidityOwnershipImportLegalityOrSceneReachabilityProven'] is False, 'Bounded original UID-counter domain')
    profiles = [{'occupied': count, 'inputWord': fword(mode), 'partyAlias': False} for count in (100, 99, 98, 97, 0) for mode in (0, 1, 2)]
    profiles += [{'occupied': 1, 'inputWord': fword(mode), 'partyAlias': True} for mode in (0, 1, 2)]
    profiles += [{'occupied': 99, 'inputWord': raw, 'partyAlias': False} for raw in
        (0x80000000, fword(3), fword(-1), 0x7F800000, 0xFF800000, 0x7FC12345, 0x7FA54321, 1)]
    instructions = {row['pc']: row for row in data['instructions'] if row['pc'] < 544}
    calls, nested, covered, outcomes = 0, 0, set(), {}
    for ordinal, case in enumerate(proof['cases']):
        thread, index = divmod(ordinal, 26)
        profile, seed = profiles[index], 2026103042000 + ordinal
        require((case['thread'], case['seed']) == (thread, seed) and case['profile'] == profile, 'Independent count/mode/alias scenario')
        state = bytearray(0x7040)
        for row in range(profile['occupied']):
            struct.pack_into('<I', state, 0x021BD674 - native.PERSIST + row * 132 + 20, (0x80000000, 0x12345678, 0xFFFFFFFF, 1)[row % 4])
        if profile['partyAlias']:
            for address in (0x021BD540, 0x021BD54C):
                struct.pack_into('<3I', state, address - native.PERSIST, *([0x80000000] * 3))
        registers = bytearray(random.Random(seed ^ 0xC17).randbytes(1024))
        require(case['initialRegisterFileHex'] == registers.hex(), 'Full raw initial register state')
        observed = case['observations']
        shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([row['entry'] for row in observed[:len(startup)]] == startup, 'Actual native start/forks')
        cursor = len(startup)
        for iteration, name in enumerate(('first', 'second')):
            if iteration:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0'), 'Natural serialized reentry')
                cursor += 1
            part = case[name]
            require(part['initialRegisterFileHex'] == registers.hex(), 'Module state carried between calls')
            args, pc, condition, trace, stores, samples = [profile['inputWord']], 0, None, [], [], []
            counter_returns = []
            while True:
                row = instructions[pc]
                op, raw = row['opcode'], row['argumentsRaw']
                following = pc + row['bytes']

                def operand(mode, value):
                    if mode == 0:
                        return struct.unpack_from('<I', registers, int(number(value)) * 4)[0]
                    if mode == 1:
                        require(number(value) == 0, 'Only declared argument word0')
                        return args[0]
                    require(mode == 2, 'Typed scalar operand mode')
                    return value

                if op == 1036:
                    following = raw[1]
                elif op == 1045:
                    value = operand(raw[3], raw[4])
                    slot = int(number(raw[2]))
                    if raw[1] == 0:
                        require(slot in (0, 1, 2), 'Only three explicit module stores')
                        struct.pack_into('<I', registers, slot * 4, value)
                        stores.append({'address': hex(native.CTX + 0x50 + slot * 4), 'bytes': 4, 'value': value})
                    else:
                        require(raw[1] == 1 and slot == 0, 'Only scalar return argument write')
                        args[0] = value
                elif op in (1039, 1044):
                    left, right = number(operand(raw[1], raw[2])), number(operand(raw[3], raw[4]))
                    condition = left == right if op == 1039 else left <= right
                elif op == 1038:
                    require(condition is not None, 'Condition dominates branch')
                    outcomes.setdefault(pc, set()).add(not condition)
                    following = raw[1] if not condition else following
                elif op == 187:
                    args[0] = fword(100 - profile['occupied'])
                    samples.append(args[0])
                    party = 3 if profile['partyAlias'] else 0
                    counter_returns += [{'nativeCallee': hex(target), 'actualNativeReturnPc': hex(address), 'resultWord': result} for target, address, result in
                        ((0x020629E0, 0x02052DCC, profile['occupied']), (0x02062AA0, 0x02052DD4, party), (0x02062AD0, 0x02052DDC, party),
                        (0x02062AA0, 0x02052DE8, party), (0x02062AD0, 0x02052DF0, party))]
                else:
                    require(op == 1026, 'Supported complete capacity instruction')
                    following = pc
                trace.append({'pc': pc, 'opcode': op, 'nextPc': following})
                require(len(trace) <= 40, 'Complete capacity trace bound')
                if op == 1026:
                    break
                pc = following
            mode = next((value for value in (0, 1, 2) if number(profile['inputWord']) == value), None)
            result = fword(int(mode is not None and 100 - profile['occupied'] >= mode + 1))
            require(part['trace'] == trace and part['completeOwnEntryReturned'] is True and part['privateReturnPc'] == 540,
                'Complete private capacity entry return')
            require(args[0] == result == part['returnedScalarWord'] and part['queryResultWords'] == samples
                and part['nativeCounterReturns'] == counter_returns and part['uidLookupWords'] ==
                ([] if not samples else [0x80000000 if profile['partyAlias'] else 0] * 12), 'Raw decision/query/five-real-counter/full-UID ABI')
            require(part['finalRegisterFileSha256'] == digest(registers) and part['orderedModuleStores'] == stores and part['persistentSha256'] == digest(state)
                and part['allOther253SlotsPreserved'] is True and part['moduleSlotsAreNotPrivateLocals'] is True, 'Exact shared module/253-neighbor/record-state effects')
            for row, step in zip(observed[cursor:cursor + len(trace)], trace):
                require(row['entry'] == ('0x204c5a0' if step['opcode'] >= 1024 else '0x205a65c') and row['resultWord'] == 1
                    and row['persistentSha256'] == digest(state), 'Actual native interpreter return/persistent state')
            cursor += len(trace)
            nested += len(counter_returns)
            covered.update(row['pc'] for row in trace)
        require(cursor == len(observed) == case['actualReturningCalls'], 'Native startup/fork/reentry/record accounting')
        calls += cursor
    require(len(outcomes) == 6 and all(values == {False, True} for values in outcomes.values()) and sorted(covered) == report['boundariesAndStorage']['allOwnRecordPcs'],
        'All six branch outcomes/all own records')
    require(calls == proof['actualReturningCalls'] == 3404 and proof['completeOwnEntryExecutions'] == 208
        and report['pairedNativeReturningCalls'] == 6808 and report['pairedCompleteOwnEntryExecutions'] == 416
        and report['pairedActualNestedCounterReturns'] == nested * 2 == 1520, 'Separate native/complete/nested counter totals')


def validate(root=ROOT, report_path=None):
    require(Path(root).resolve() == ROOT and sys.version_info[:3] == (3, 13, 5), 'Local pinned Python')
    path = checked(ROOT, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(row.value) for row in ast.parse(path.read_text()).body if isinstance(row, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'PINS' for target in row.targets))
    for name, pin in pins.items():
        checked(ROOT, {'path': name, 'sha256': pin})
    module = shared.helpers.load_module(path, '_record_capacity_matcher')
    for name, pin in (('extract/arm9/arm9.bin', module.fixtures.native.MAIN_HASH), ('extract/arm9_overlays/ov000.bin', module.fixtures.native.OVERLAY_HASH),
            ('extract/arm9/itcm.bin', module.fixtures.native.ITCM_HASH)):
        checked(ROOT, {'path': name, 'sha256': pin})
    module.assets.original_files.cache_clear()
    data = module.assets.load(ROOT / 'extract/files/world.e')
    report = json.loads(local(ROOT, REPORT if report_path is None else report_path).read_text())
    require(report['evidenceClass'] == 'ordinary-C-complete-native-record-capacity-decision-SCR-source-match' and report['generator'] == MATCHER
        and report['generatorSha256'] == MATCHER_HASH and report['sourceClosure'] == [{'path': name, 'sha256': pin} for name, pin in pins.items()], 'Frozen capacity source/generator closure')
    unused, files = module.assets.original_files()
    require(report['romSha256'] == module.assets.ROM_HASH and report['romFileRange'] == list(files['world.e']) and report['archiveSha256'] == data['assetSha256']
        and report['scriptSha256'] == data['scriptSha256'] and report['codeSha256'] == digest(data['code'])
        and report['nativeSourceRoot'] == str(ROOT) == str(module.fixtures.native.ROOT), 'Current original ROM/image/native-root identity')
    require(report['boundariesAndStorage'] == module.boundary(data), 'Current complete/direct/module/argument boundaries')
    build = report['sourceOnlyBuild']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False and build['cwd'] == str(ROOT / 'work/script-source/20261030/batch21/record-capacity/source-only')
        and build['command'] == [sys.executable, 'scr_c_compiler_20261030_v17.py', '--source', 'evaluate_record_capacity.c', '--base', '0',
        '--bindings', 'objects.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json'], 'Actual capacity source-only invocation')
    inputs = {Path(row['path']).name: checked(ROOT, row) for row in build['inputs']}
    require(len(inputs) == len(build['inputs']) == 6, 'Complete six-file capacity compiler/source closure')
    for name, copied in inputs.items():
        origin = name if name.endswith('.py') else 'src/scripts/20261030/batch21/' + name
        require(digest(copied.read_bytes()) == pins[origin], 'Copied frozen capacity source-only input')
    body = checked(ROOT, build['emittedBody']).read_bytes()
    compiled = json.loads(checked(ROOT, build['compilerReport']).read_text())
    require(body == data['code'][:544] and compiled == build['compilerEvidence'] and compiled['generalCCompilerClaimed'] is False
        and compiled['sourceReturnType'] == 'float' and compiled['moduleAndArgumentObjectsAreNotPrivateLocals'] is True,
        'Complete544B raw-float/global source product')
    stage = ROOT / 'work/script-source/20261030/batch21/validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=stage) as temporary:
        directory = Path(temporary)
        for name, copied in inputs.items():
            shutil.copyfile(copied, directory / name)
        subprocess.run(build['command'], cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        require((directory / 'generated.scrfunc').read_bytes() == body and json.loads((directory / 'build.json').read_text()) == compiled, 'Fresh isolated capacity source rebuild')
    require(report['matchedRange'] == {'startPc': 0, 'endExclusivePc': 544, 'bytes': 544, 'sha256': digest(body)}
        and checked(ROOT, build['rebuiltImage']).read_bytes() == data['script'], 'Complete current source range/image')
    instructions = {row['pc']: row for row in data['instructions'] if row['pc'] < 544}
    for access in compiled['objectAccesses']:
        row = instructions[access['instructionPc']]
        raw, op = row['argumentsRaw'], row['opcode']
        if access['access'] == 'write':
            require(op == 1045 and (raw[1], raw[2]) == (access['bank'], fword(access['slot'])), 'Exact compiler object write-PC')
        else:
            operands = [(raw[3], raw[4])] if op == 1045 else [(raw[1], raw[2]), (raw[3], raw[4])] if op in (1039, 1044) else []
            require((access['bank'], fword(access['slot'])) in operands, 'Exact compiler object read-PC')
    require(len(report['compilerControls']) == 10, 'Ten source/type/namespace/storage controls')
    for row in report['compilerControls']:
        source = checked(ROOT, row['source'])
        require(checked(ROOT, row['header']) == source.parent / 'scr_record_capacity.h', 'Control include closure')
        try:
            module.compiler.compile_source(source, 0, row['bindings'])
        except ValueError as error:
            require(str(error) == row['error'] and row['rejectedBeforeOutput'] is True, 'Actual source/type/namespace/storage rejection')
        else:
            raise ValueError('Invalid capacity source compiled')
    native_proof(report, module, data)
    require(report['nativeCounterIdentity'] == {'syscall': 187, 'handler': 'main:ARM02052DBC', 'counter': 'main:ARM020629E0',
        'secondaryCounters': ['main:ARM02062AA0', 'main:ARM02062AD0'], 'recordBase': '0x21bd674', 'recordStride': 132, 'recordCount': 100, 'testedNonzeroWordOffset': 20}, 'Qualified original count identity')
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1 and report['qualifiedScriptRangeBytes'] == 544
        and report['originalScaffoldingBytes'] == len(data['script']) - 544 and report['nativeRecordValidityOwnershipImportLegalityOrNaturalSceneReachabilityProven'] is False
        and all(report[name] == 0 for name in ('scaffoldingSourceCredit', 'nativeExecutableByteCredit', 'completeImagesRecovered', 'nativeFunctionStubs'))
        and report['postFaultStateUsedForProof'] is False and report['wholeRomSourceMatch'] is False
        and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'One bounded definition/zero excess semantic or byte credit')
    return {(digest(data['code']), 0): {'codeSha256': digest(data['code']), 'scriptSha256': data['scriptSha256'], 'startPc': 0, 'endExclusivePc': 544,
        'bytes': 544, 'sha256': digest(body), 'entryAliases': [279], 'sourceSha256': compiled['sourceSha256'], 'function': compiled['function'],
        'pairedCompleteOwnEntryExecutions': 416, 'pairedNativeReturningCalls': 6808, 'pairedActualNestedCounterReturns': 1520,
        'moduleGlobalSlots': [0, 1, 2], 'privateLocalSlots': [], 'argumentBankLiveIns': [0], 'argumentBankCallClobbers': [0]}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(row['bytes'] for row in units.values())}))
