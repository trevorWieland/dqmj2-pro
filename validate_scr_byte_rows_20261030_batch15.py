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
SPEC = importlib.util.spec_from_file_location('_byte_rows_shared', SHARED)
shared = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_byte_rows_20261030_batch15.py'
MATCHER_HASH = '03aeeff13f6cb7e85034ffb968bb2472b3b0629e4554bad69adf47706d2fc3c0'
REPORT = 'evidence/matches/scripts-20261030-byte-rows.json'


def invocation(matcher, part, observed, guarded, registers, persistent, instructions):
    pc, arguments, expected = 50684, [0] * 5, bytearray(guarded[4:68])
    trace, configured, stores = [], [], []
    require(part['guardedRowsBeforeHex'] == guarded.hex() and part['registerFileBeforeHex'] == registers.hex(),
        'Complete table/register-file carry')
    for observation in observed:
        row = instructions[pc]
        opcode, raw = row['opcode'], row['argumentsRaw']
        following = pc + row['bytes']
        if opcode == 1036:
            following = raw[1]
        elif opcode == 1045:
            register = int(matcher.assets.f32(raw[2]))
            require(raw[1] == 1 and raw[3] == 2 and 0 <= register < 5, 'Only five constant API argument words')
            arguments[register] = int(matcher.assets.f32(raw[4]))
        elif opcode == 102:
            require(tuple(arguments) == matcher.fixtures.PRESETS[len(configured)], 'All twelve source byte-row presets')
            logical, *values = arguments
            physical = matcher.fixtures.MAPPING[logical]
            expected[physical * 4:physical * 4 + 4] = bytes(values)
            configured.append({'pc': pc, 'logicalIndex': logical, 'nativeRow': physical, 'bytes': list(values)})
            stores += [{'address': hex(0x020E2CF4 + physical * 4 + lane), 'bytes': 1, 'value': value} for lane, value in enumerate(values)]
        else:
            require(opcode == 1026, 'Supported configuration record')
            following = pc
        require(observation['entry'] == ('0x204c5a0' if opcode >= 1024 else '0x205a65c') and observation['resultWord'] == 1
            and observation['persistentSha256'] == digest(persistent), 'Actual returning native call/persistent invariance')
        trace.append({'pc': pc, 'opcode': opcode, 'nextPc': following})
        pc = following
    require(len(trace) == 74 and trace[-1]['pc'] == 52232 and trace[-1]['opcode'] == 1026 and part['completeEntryReturned'] is True
        and part['privateReturnPc'] == 52232, 'Complete74-record/private-return execution')
    require(part['trace'] == trace and part['configuredRows'] == configured and part['orderedNativeByteStores'] == stores
        and part['byteRowsAfterHex'] == expected.hex(), 'Every preset/ordered byte store/all table effects')
    require(part['persistentInvariantSha256'] == digest(persistent) and part['registerFileAfterSha256'] == digest(registers)
        and part['all256SlotsAndWordGuardsPreserved'] is True, 'All256 slots/guards/persistent preservation')
    return guarded[:4] + bytes(expected) + guarded[68:]


def native_proof(matcher, report, data):
    proof = report['differential']
    require(len(proof['cases']) == proof['freshMachines'] == 32 and proof['providerCount'] == 0
        and proof['nativeInstructionCap'] == 20000 and proof['nativeTimeoutMicroseconds'] == 1000000 and proof['scriptStepCap'] == 100
        and proof['serializedCompleteCallsOnly'] is True and proof['configurationOnly'] is True
        and proof['branchDecisionLogicClaimed'] is False and proof['naturalSceneOrRenewabilityMeaningProven'] is False,
        'Bounded configuration/thread population and scope')
    instructions = {row['pc']: row for row in data['instructions'] if 50684 <= row['pc'] < 52236}
    calls, executed = 0, set()
    for index, case in enumerate(proof['cases']):
        thread, pattern, seed = index // 8, matcher.fixtures.PATTERNS[index % 8], 2026103024000 + index
        require((case['thread'], case['pattern'], case['seed'], case['providerCount']) == (thread, pattern, seed, 0), 'Fresh native scenario identity')
        persistent = random.Random(seed).randbytes(0x7040)
        registers = random.Random(seed ^ 0xC15A).randbytes(1024)
        guarded = matcher.fixtures.guarded_rows(pattern, seed)
        require(case['initialRegisterFileHex'] == registers.hex() and case['initialGuardedRowsHex'] == guarded.hex(),
            'Independent initial table/register seed')
        observed = case['observations']
        shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([row['entry'] for row in observed[:len(startup)]] == startup, 'Native init/start/forks')
        cursor = len(startup)
        for ordinal, name in enumerate(('first', 'second')):
            if ordinal:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0'), 'Natural serialized reentry')
                cursor += 1
            part = case[name]
            end = cursor + len(part['trace'])
            guarded = invocation(matcher, part, observed[cursor:end], guarded, registers, persistent, instructions)
            cursor = end
            executed.update(row['pc'] for row in part['trace'])
        require(cursor == len(observed) == case['actualReturningCalls'], 'Actual per-case native return counts')
        calls += cursor
    require(proof['executedOwnRecordPcs'] == sorted(executed) == report['boundariesAndStorage']['reachableOwnRecordPcs'], 'All own configuration records executed')
    require(proof['actualReturningCalls'] == calls and report['pairedNativeReturningCalls'] == calls * 2
        and proof['completeEntryExecutions'] == 64 and report['pairedCompleteOwnEntryExecutions'] == 128,
        'Separate complete-entry/native return totals')


def compiler_controls(matcher, report):
    proof = report['compilerControls']
    require(len(proof['rejectedSourceProfiles']) == 7 and proof['controlSourceCredit'] == 0, 'Source/domain/namespace rejection population')
    for case in proof['rejectedSourceProfiles']:
        source = checked(ROOT, case['source'])
        require((source.parent / 'scr_byte_rows.h').read_bytes() == (matcher.SOURCE / 'scr_byte_rows.h').read_bytes(), 'Control ABI header closure')
        try:
            matcher.compiler.compile_source(source, 50684)
        except ValueError as error:
            require(str(error) == case['error'] and case['rejectedBeforeOutput'] is True, 'Actual source rejection')
        else:
            raise ValueError('Unsupported byte-row source compiled')
    patterns = ((0, 0, 0, 0), (255, 255, 255, 255), (0, 1, 128, 255), (255, 128, 1, 0), (1, 2, 3, 4))
    require(len(proof['all95LogicalByteCases']) == 95, 'All19 indices/five byte-pattern controls')
    calls = 0
    for index, case in enumerate(proof['all95LogicalByteCases']):
        logical, values = index // 5, patterns[index % 5]
        source = checked(ROOT, case['source'])
        body, compiled = matcher.compiler.compile_source(source, 0)
        require(json.loads(json.dumps(compiled)) == case['compilerEvidence'] and len(body) == 144, 'Fresh synthetic byte-row source build')
        row = matcher.fixtures.MAPPING[logical]
        expected = bytearray([0xA5]) * 72
        expected[4 + row * 4:8 + row * 4] = bytes(values)
        stores = [{'address': hex(0x020E2CF4 + row * 4 + lane), 'bytes': 1, 'value': value} for lane, value in enumerate(values)]
        require((case['logicalIndex'], tuple(case['values']), case['nativeRow']) == (logical, values, row)
            and case['expectedGuardedRowsHex'] == expected.hex() and case['orderedNativeByteStores'] == stores
            and case['completeControlReturned'] is True and case['sourceCredit'] == 0, 'All original index aliases/byte values/ordered stores')
        shared.observations(case['observations'])
        require(case['actualReturningCalls'] == len(case['observations']) == len(case['trace']) + 2 and case['trace'][-1]['opcode'] == 1026,
            'Separate actual control returns')
        calls += case['actualReturningCalls']
    require(calls == proof['rowControlNativeReturns'] == report['separateRowControlNativeReturns'], 'Separate row-control return totals')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Local pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(row.value) for row in ast.parse(path.read_text()).body if isinstance(row, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'PINS' for target in row.targets))
    for name, pin in pins.items():
        checked(root, {'path': name, 'sha256': pin})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_byte_rows_frozen_matcher')
    for name, pin in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
            ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH), ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': pin})
    matcher.assets.original_files.cache_clear()
    data = matcher.assets.load(root / 'extract/files/world.e')
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['evidenceClass'] == 'ordinary-C-complete-native-byte-row-configuration-SCR-source-match'
        and report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH and report['sourceClosure'] ==
        [{'path': name, 'sha256': pin} for name, pin in pins.items()], 'Frozen source class/generator/closure')
    rom, files = matcher.assets.original_files()
    interval = files['world.e']
    require((root / data['asset']).read_bytes() == rom[interval[0]:interval[1]] and report['romSha256'] == matcher.assets.ROM_HASH
        and report['romFileRange'] == list(interval) and report['archiveSha256'] == data['assetSha256']
        and report['scriptSha256'] == data['scriptSha256'] and report['codeSha256'] == digest(data['code']), 'Current original ROM/image identity')
    require(report['boundariesAndStorage'] == matcher.boundary(data) and report['nativeContracts'] == matcher.native_contracts(),
        'Current direct/private/argument-only bounds and native ABI')
    build = report['sourceOnlyBuild']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False and build['cwd'] ==
        str(root / 'work/script-source/20261030/batch15/byte-rows/source-only') and build['command'] ==
        [sys.executable, 'scr_c_compiler_20261030_v13.py', '--source', 'initialize_context_byte_rows.c', '--base', hex(50684),
        '--output', 'generated.scrfunc', '--report', 'build.json'], 'Actual source-only command/directory')
    inputs = {Path(case['path']).name: checked(root, case) for case in build['inputs']}
    require(len(inputs) == len(build['inputs']) == 4, 'Complete source-only closure')
    for name, path in inputs.items():
        origin = name if name.endswith('.py') else 'src/scripts/20261030/batch15/' + name
        require(digest(path.read_bytes()) == pins[origin], 'Copied source-only input identity')
    body = checked(root, build['emittedBody']).read_bytes()
    compiled = json.loads(checked(root, build['compilerReport']).read_text())
    require(body == data['code'][50684:52236] and compiled == build['compilerEvidence'] and compiled['generalCCompilerClaimed'] is False
        and compiled['configurationOnly'] is True and compiled['sourceContainsBranches'] is False, 'Complete1552B ordinary configuration source')
    stage = root / 'work/script-source/20261030/batch15/validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for name, path in inputs.items():
            shutil.copyfile(path, directory / name)
        subprocess.run(build['command'], cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        require((directory / 'generated.scrfunc').read_bytes() == body and json.loads((directory / 'build.json').read_text()) == compiled,
            'Fresh isolated source-only rebuild')
    require(report['matchedRange'] == {'startPc': 50684, 'endExclusivePc': 52236, 'bytes': 1552, 'sha256': digest(body)}
        and checked(root, build['rebuiltImage']).read_bytes() == data['script'], 'Complete current source range/image')
    compiler_controls(matcher, report)
    native_proof(matcher, report, data)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1 and report['qualifiedScriptRangeBytes'] == 1552
        and report['originalScaffoldingBytes'] == len(data['script']) - 1552 and report['configurationOnly'] is True
        and report['branchDecisionLogicClaimed'] is False, 'One configuration source family scope')
    require(all(report[key] == 0 for key in ('scaffoldingSourceCredit', 'nativeExecutableByteCredit', 'completeImagesRecovered', 'nativeFunctionStubs'))
        and report['postFaultStateUsedForProof'] is False and report['wholeRomSourceMatch'] is False
        and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'Zero excess/post-fault source credit')
    return {(digest(data['code']), 50684): {'codeSha256': digest(data['code']), 'scriptSha256': data['scriptSha256'], 'asset': data['asset'],
        'startPc': 50684, 'endExclusivePc': 52236, 'bytes': 1552, 'sha256': digest(body), 'entryAliases': [11], 'mode': 'SCR', 'vmHostProcessor': 'ARM9',
        'source': 'src/scripts/20261030/batch15/initialize_context_byte_rows.c', 'sourceSha256': compiled['sourceSha256'], 'sourceDefinitionCount': 1,
        'pairedCompleteOwnEntryExecutions': report['pairedCompleteOwnEntryExecutions'], 'pairedNativeReturningCalls': report['pairedNativeReturningCalls'],
        'wholeImageReconstructed': False, 'configurationOnly': True, 'branchDecisionLogicClaimed': False}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(row['bytes'] for row in units.values())}))
