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
SPEC = importlib.util.spec_from_file_location('_byte_modes_shared', SHARED)
shared = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_byte_modes_20261030_batch14.py'
MATCHER_HASH = 'f47a610f68ab4c3c1506fb264b5bef6fb0ca4548eb32d90525e01645db6bfbfb'
REPORT = 'evidence/matches/scripts-20261030-byte-modes.json'


def invocation(matcher, part, observations, registers, guarded_rows, flags, input_word, persistent, instructions):
    pc, args, expected = 52244, [input_word, 0], bytearray(guarded_rows[4:68])
    trace, reads, selections, branches, stores = [], [], [], [], []
    conditions = {site: not flags & (1 << bit) for bit, site in enumerate((52360, 52520, 52680, 52840, 53000, 53160))}
    require(part['inputWord'] == input_word and part['registerFileBeforeHex'] == bytes(registers).hex()
        and part['byteRowsBeforeHex'] == guarded_rows.hex(), 'Raw formal/all256-slot/full-table carry')
    for observation in observations:
        row = instructions[pc]
        op, raw, size = row['opcode'], row['argumentsRaw'], row['bytes']
        following = pc + size
        if op == 1036:
            following = raw[1]
        elif op == 1038:
            taken = not conditions[pc]
            following = raw[1] if taken else following
            branches.append({'pc': pc, 'takenToEncodedTarget': taken})
        elif op == 1045:
            mode, destination = raw[1], int(matcher.assets.f32(raw[2]))
            if mode == 1:
                require(raw[3] == 2 and destination in (0, 1), 'Exact byte-mode constant arguments')
                args[destination] = raw[4]
            else:
                require(mode == 0 and destination in (81, 82) and raw[3:] == [1, 0], 'Exact formal/getter captures')
                struct.pack_into('<I', registers, destination * 4, args[0])
        elif op == 41:
            index = int(matcher.assets.f32(args[0]))
            require(index in matcher.fixtures.FLAGS, 'Qualified primary predicates')
            enabled = bool(flags & (1 << matcher.fixtures.FLAGS.index(index)))
            reads.append({'pc': pc, 'index': index, 'enabled': enabled})
            args[0] = matcher.fixtures.fword(int(enabled))
        elif op == 103:
            index, mode = (int(matcher.assets.f32(value)) for value in args)
            require(index in matcher.fixtures.LOGICAL and mode == 0, 'Exact byte-mode API domains')
            native_row = matcher.fixtures.MAPPING[index]
            expected[native_row * 4:native_row * 4 + 4] = bytes([100, 0, 0, 0])
            selections.append({'pc': pc, 'logicalIndex': index, 'nativeRow': native_row, 'mode': mode})
            stores += [{'address': hex(0x020E2CF4 + native_row * 4 + lane), 'bytes': 1, 'value': 100 if lane == 0 else 0}
                for lane in range(4)]
        elif op == 1026:
            following = pc
        else:
            require(op == 1039, 'Supported primary byte-mode record')
        require(observation['entry'] == ('0x204c5a0' if op >= 1024 else '0x205a65c') and observation['resultWord'] == 1
            and observation['persistentSha256'] == digest(persistent), 'Actual native return/persistent effect per record')
        trace.append({'pc': pc, 'opcode': op, 'nextPc': following})
        pc = following
    require(trace[-1]['pc'] == 53240 and trace[-1]['opcode'] == 1026 and part['completeEntryReturned'] is True
        and part['privateReturnPc'] == 53240, 'Complete private-return termination')
    require(part['trace'] == trace and part['reads'] == reads and part['selections'] == selections and part['branches'] == branches,
        'Every actual primary/branch/byte-mode selection')
    require(part['orderedNativeByteStores'] == stores and part['byteRowsAfterHex'] == expected.hex(), 'Ordered four-byte copies/full-table effects')
    require(part['capturedFormalWord'] == input_word and part['registerFileAfterSha256'] == digest(registers)
        and part['allOtherSlotsAndTableGuardsPreserved'] is True and part['persistentInvariantSha256'] == digest(persistent),
        'Raw formal/other slots/guards/persistent invariant')
    return guarded_rows[:4] + bytes(expected) + guarded_rows[68:]


def native_proof(matcher, report, data):
    proof = report['differential']
    require(len(proof['cases']) == proof['freshMachines'] == 256 and proof['providerCount'] == 0
        and proof['nativeInstructionCap'] == 20000 and proof['nativeTimeoutMicroseconds'] == 1000000
        and proof['scriptStepCap'] == 128 and proof['serializedCompleteCallsOnly'] is True
        and proof['naturalSceneOrRenewabilityMeaningProven'] is False and proof['formalRawWords'] == list(matcher.fixtures.ARGUMENTS),
        'Bounded complete primary/formal population and scope')
    instructions = {row['pc']: row for row in data['instructions'] if 52244 <= row['pc'] < 53244}
    calls, records, branches = 0, set(), {}
    for index, case in enumerate(proof['cases']):
        thread, flags, seed = index // 64, index % 64, 2026103022000 + index
        require((case['thread'], case['flags'], case['seed'], case['providerCount']) == (thread, flags, seed, 0), 'Fresh typed flags/thread population')
        state = bytearray(random.Random(seed).randbytes(0x7040))
        for bit, flag in enumerate(matcher.fixtures.FLAGS):
            matcher.fixtures.native.bit_set(state, matcher.fixtures.native.PRIMARY, flag, bool(flags & (1 << bit)))
        registers = bytearray(random.Random(seed ^ 0xC81).randbytes(1024))
        guarded = random.Random(seed ^ 0x103).randbytes(72)
        require(case['initialRegisterFileHex'] == registers.hex() and case['initialGuardedByteRowsHex'] == guarded.hex(), 'Independent seeded table/register state')
        observed = case['observations']
        shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([row['entry'] for row in observed[:len(startup)]] == startup, 'Native init/start/forks')
        cursor = len(startup)
        for ordinal, name in enumerate(('first', 'second')):
            if ordinal:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0'), 'Natural serialized reentry')
                cursor += 1
            argument = matcher.fixtures.ARGUMENTS[(flags + (3 if ordinal else 0)) % 8]
            part = case[name]
            end = cursor + len(part['trace'])
            guarded = invocation(matcher, part, observed[cursor:end], registers, guarded, flags, argument, bytes(state), instructions)
            cursor = end
            records.update(row['pc'] for row in part['trace'])
            for row in part['branches']:
                branches.setdefault(str(row['pc']), set()).add(row['takenToEncodedTarget'])
        require(cursor == len(observed) == case['actualReturningCalls'], 'Actual per-case native-return count')
        calls += cursor
    require(all(values == {False, True} for values in branches.values()) and proof['branchCoverage'] ==
        {pc: sorted(values) for pc, values in branches.items()}, 'Both outcomes of all six primary predicates')
    require(proof['executedOwnRecordPcs'] == sorted(records) == report['boundariesAndStorage']['reachableOwnRecordPcs'], 'All own records executed')
    require(proof['actualReturningCalls'] == calls and report['pairedNativeReturningCalls'] == calls * 2
        and proof['completeEntryExecutions'] == 512 and report['pairedCompleteOwnEntryExecutions'] == 1024,
        'Separate complete-entry/native counts')


def controls(matcher, report):
    proof = report['compilerControls']
    require(len(proof['rejectedSourceProfiles']) == 8 and proof['controlSourceCredit'] == 0, 'Source/domain/type rejection population')
    for row in proof['rejectedSourceProfiles']:
        source = checked(ROOT, row['source'])
        require((source.parent / 'scr_byte_mode.h').read_bytes() == (matcher.SOURCE / 'scr_byte_mode.h').read_bytes(), 'Control header closure')
        try:
            matcher.compiler.compile_source(source, 52244, row['bindings'])
        except ValueError as error:
            require(str(error) == row['error'] and row['rejectedBeforeOutput'] is True, 'Actual source rejection')
        else:
            raise ValueError('Unsupported byte-mode source compiled')
    require(len(proof['all76LogicalModeCases']) == 76, 'All logical19/mode4 controls')
    calls = 0
    for index, case in enumerate(proof['all76LogicalModeCases']):
        logical, mode = index // 4, index % 4
        source = checked(ROOT, case['source'])
        body, compiled = matcher.compiler.compile_source(source, 0, {'locals': {'input': 0}, 'globals': {}})
        require(json.loads(json.dumps(compiled)) == case['compilerEvidence'] and len(body) == 96, 'Fresh source-only mode control')
        native_row = matcher.fixtures.MAPPING[logical]
        expected = bytearray([0xA5]) * 72
        expected[4 + native_row * 4:8 + native_row * 4] = bytes(100 if lane == mode else 0 for lane in range(4))
        stores = [{'address': hex(0x020E2CF4 + native_row * 4 + lane), 'bytes': 1, 'value': 100 if lane == mode else 0} for lane in range(4)]
        require((case['logicalIndex'], case['mode'], case['nativeRow']) == (logical, mode, native_row)
            and case['expectedGuardedRowsHex'] == expected.hex() and case['orderedNativeByteStores'] == stores
            and case['completeControlReturned'] is True and case['sourceCredit'] == 0, 'Every native index mapping/mode/ordered byte-copy control')
        shared.observations(case['observations'])
        require(case['actualReturningCalls'] == len(case['observations']) == len(case['trace']) + 2
            and case['trace'][-1]['opcode'] == 1026, 'Control native actual returns')
        calls += case['actualReturningCalls']
    require(calls == proof['modeControlNativeReturns'] == report['separateModeControlNativeReturns'], 'Separate mode-control return totals')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Local pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(row.value) for row in ast.parse(path.read_text()).body if isinstance(row, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'PINS' for target in row.targets))
    for name, pin in pins.items():
        checked(root, {'path': name, 'sha256': pin})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_byte_modes_frozen_matcher')
    for name, pin in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
            ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH), ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': pin})
    matcher.assets.original_files.cache_clear()
    data = matcher.assets.load(root / 'extract/files/world.e')
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['evidenceClass'] == 'ordinary-C-complete-primary-conditional-byte-mode-SCR-source-match'
        and report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH and report['sourceClosure'] ==
        [{'path': name, 'sha256': pin} for name, pin in pins.items()], 'Frozen complete source class/generator/closure')
    rom, files = matcher.assets.original_files()
    interval = files['world.e']
    require((root / data['asset']).read_bytes() == rom[interval[0]:interval[1]] and report['romSha256'] == matcher.assets.ROM_HASH
        and report['romFileRange'] == list(interval) and report['archiveSha256'] == data['assetSha256']
        and report['scriptSha256'] == data['scriptSha256'] and report['codeSha256'] == digest(data['code']), 'Current original ROM/image identity')
    require(report['boundariesAndStorage'] == matcher.boundary(data) and report['nativeContracts'] == matcher.native_contracts(), 'Current direct/private/slot bounds and native ABI')
    build = report['sourceOnlyBuild']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False and build['cwd'] ==
        str(root / 'work/script-source/20261030/batch14/byte-modes/source-only') and build['command'] ==
        [sys.executable, 'scr_c_compiler_20261030_v12.py', '--source', 'apply_primary_byte_modes.c', '--base', hex(52244),
        '--bindings', 'modes.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json'], 'Actual source-only command/directory')
    inputs = {Path(row['path']).name: checked(root, row) for row in build['inputs']}
    require(len(inputs) == len(build['inputs']) == 7, 'Complete source-only closure')
    for name, path in inputs.items():
        origin = name if name.endswith('.py') else 'src/scripts/20261030/batch14/' + name
        require(digest(path.read_bytes()) == pins[origin], 'Copied source-only identity')
    body = checked(root, build['emittedBody']).read_bytes()
    compiled = json.loads(checked(root, build['compilerReport']).read_text())
    require(body == data['code'][52244:53244] and compiled == build['compilerEvidence'] and compiled['generalCCompilerClaimed'] is False,
        'Complete1000B ordinary source product')
    stage = root / 'work/script-source/20261030/batch14/validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for name, path in inputs.items():
            shutil.copyfile(path, directory / name)
        subprocess.run(build['command'], cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        require((directory / 'generated.scrfunc').read_bytes() == body and json.loads((directory / 'build.json').read_text()) == compiled,
            'Fresh isolated source-only rebuild')
    require(report['matchedRange'] == {'startPc': 52244, 'endExclusivePc': 53244, 'bytes': 1000, 'sha256': digest(body)}
        and checked(root, build['rebuiltImage']).read_bytes() == data['script'], 'Complete current source range/image')
    controls(matcher, report)
    native_proof(matcher, report, data)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1 and report['qualifiedScriptRangeBytes'] == 1000
        and report['originalScaffoldingBytes'] == len(data['script']) - 1000, 'One complete source scope')
    require(all(report[key] == 0 for key in ('scaffoldingSourceCredit', 'nativeExecutableByteCredit', 'completeImagesRecovered', 'nativeFunctionStubs'))
        and report['postFaultStateUsedForProof'] is False and report['wholeRomSourceMatch'] is False
        and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'Zero excess/post-fault source credit')
    return {(digest(data['code']), 52244): {'codeSha256': digest(data['code']), 'scriptSha256': data['scriptSha256'], 'asset': data['asset'],
        'startPc': 52244, 'endExclusivePc': 53244, 'bytes': 1000, 'sha256': digest(body), 'entryAliases': [12],
        'mode': 'SCR', 'vmHostProcessor': 'ARM9', 'source': 'src/scripts/20261030/batch14/apply_primary_byte_modes.c',
        'sourceSha256': compiled['sourceSha256'], 'sourceDefinitionCount': 1,
        'pairedCompleteOwnEntryExecutions': report['pairedCompleteOwnEntryExecutions'],
        'pairedNativeReturningCalls': report['pairedNativeReturningCalls'], 'wholeImageReconstructed': False}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(row['bytes'] for row in units.values())}))
