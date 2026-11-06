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
SPEC = importlib.util.spec_from_file_location('_registered_initializer_shared', SHARED)
shared = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_registered_initializer_20261030_batch18.py'
MATCHER_HASH = 'd797fafe52ee93d09628445d7d1e0d68ac348edb8f8de624d192ab913815ace1'
REPORT = 'evidence/matches/scripts-20261030-registered-initializer.json'


def native_proof(report, matcher):
    proof, native = report['differential'], matcher.fixtures.native
    require(proof['freshMachines'] == len(proof['cases']) == 32 and proof['scriptStepCap'] == 22
        and proof['nativeInstructionCap'] == 20000 and proof['nativeTimeoutMicroseconds'] == 1000000 and proof['providerCount'] == 0
        and proof['moduleGlobalSlots'] == list(range(3, 23)) and proof['privateLocalSlots'] == [] and proof['serializedReentryChecked'] is True
        and proof['naturalInitializerOrRegistrationCallerReachabilityProven'] is False and proof['initializationOnly'] is True
        and proof['branchDecisionLogicClaimed'] is False, 'Bounded initialization-only module-global population')
    patterns = [None, (0,), (0xFFFFFFFF,), (0xBF800000,), (0x7FC12345,), (0x7FA54321,), (0x7F800000, 0xFF800000), (0, 0x80000000)]
    trace = [{'pc': 552, 'opcode': 1036, 'nextPc': 564}] + [{'pc': 564 + index * 24, 'opcode': 1045, 'nextPc': 588 + index * 24}
        for index in range(20)] + [{'pc': 1044, 'opcode': 1026, 'nextPc': 1044}]
    stores = [{'address': hex(native.CTX + 0x50 + slot * 4), 'bytes': 4, 'value': 0xBF800000} for slot in range(3, 23)]
    calls = 0
    for ordinal, case in enumerate(proof['cases']):
        thread, pattern, seed = ordinal // 8, ordinal % 8, 2026103030000 + ordinal
        require((case['thread'], case['pattern'], case['seed']) == (thread, pattern, seed), 'Independent initializer context identity')
        registers = bytearray(random.Random(seed ^ 0xC17).randbytes(1024))
        if pattern:
            values = patterns[pattern]
            for slot in range(3, 23):
                struct.pack_into('<I', registers, slot * 4, values[(slot - 3) % len(values)])
        persistent = digest(random.Random(seed).randbytes(0x7040))
        require(case['initialRegisterFileHex'] == registers.hex(), 'Raw arbitrary initial module/global and other register state')
        observed = case['observations']
        shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([row['entry'] for row in observed[:len(startup)]] == startup, 'Actual native initialization and entry/forks')
        cursor = len(startup)
        argument_hash = None
        for iteration, key in enumerate(('first', 'second')):
            if iteration:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0'), 'Actual native serialized reentry')
                cursor += 1
            part = case[key]
            require(part['initialRegisterFileHex'] == registers.hex() and part['trace'] == trace and part['completeOwnEntryReturned'] is True
                and part['privateReturnPc'] == 1044, 'Complete private initializer return')
            registers[12:92] = struct.pack('<20I', *([0xBF800000] * 20))
            require(part['finalRegisterFileSha256'] == digest(registers) and part['allOther236SlotsPreserved'] is True
                and part['moduleGlobalsAreNotPrivateLocals'] is True and part['orderedGlobalWordStores'] == stores
                and part['persistentSha256'] == persistent, 'All20 ordered global writes/236 neighbors/persistent bytes')
            encoded = part['unchangedArgumentBankSha256']
            require(len(bytes.fromhex(encoded)) == 32 and (argument_hash is None or argument_hash == encoded), 'Unchanged nonformal VM argument bank')
            argument_hash = encoded
            for row in observed[cursor:cursor + 22]:
                require(row['entry'] == '0x204c5a0' and row['resultWord'] == 1 and row['persistentSha256'] == persistent,
                    'Every actual interpreter return preserves persistent state')
            cursor += 22
        require(cursor == len(observed) == case['actualReturningCalls'] == 47 + thread, 'Per-context native startup/reentry/record count')
        calls += cursor
    require(proof['actualReturningCalls'] == calls == 1552 and proof['completeOwnEntryExecutions'] == 64
        and report['pairedCompleteOwnEntryExecutions'] == 128 and report['pairedNativeReturningCalls'] == 3104,
        'Separate complete initializer/native return totals')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Local pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(row.value) for row in ast.parse(path.read_text()).body if isinstance(row, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'PINS' for target in row.targets))
    for name, pin in pins.items():
        checked(root, {'path': name, 'sha256': pin})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_registered_initializer_matcher')
    for name, pin in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH), ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH),
            ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': pin})
    matcher.assets.original_files.cache_clear()
    data = matcher.assets.load(root / 'extract/files/world.e')
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['evidenceClass'] == 'ordinary-C-complete-module-global-float-initializer-SCR-source-match'
        and report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH
        and report['sourceClosure'] == [{'path': name, 'sha256': pin} for name, pin in pins.items()], 'Frozen initializer source/generator closure')
    unused, files = matcher.assets.original_files()
    require(report['romSha256'] == matcher.assets.ROM_HASH and report['romFileRange'] == list(files['world.e'])
        and report['archiveSha256'] == data['assetSha256'] and report['scriptSha256'] == data['scriptSha256'] and report['codeSha256'] == digest(data['code']),
        'Current original ROM/archive/image identity')
    require(report['boundariesAndStorage'] == matcher.boundary(data), 'Current full private/direct/module-global boundaries')
    build = report['sourceOnlyBuild']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False and build['cwd'] ==
        str(root / 'work/script-source/20261030/batch18/registered-initializer/source-only') and build['command'] ==
        [sys.executable, 'scr_c_compiler_20261030_v15.py', '--source', 'clear_registered_keys.c', '--base', '552', '--bindings', 'globals.bindings.json',
        '--output', 'generated.scrfunc', '--report', 'build.json'], 'Actual source-only initializer command/directory')
    inputs = {Path(row['path']).name: checked(root, row) for row in build['inputs']}
    require(len(inputs) == len(build['inputs']) == 5, 'Complete source-only initializer closure')
    for name, copied in inputs.items():
        origin = name if name.endswith('.py') else 'src/scripts/20261030/batch18/' + name
        require(digest(copied.read_bytes()) == pins[origin], 'Copied initializer source-only input')
    body = checked(root, build['emittedBody']).read_bytes()
    compiled = json.loads(checked(root, build['compilerReport']).read_text())
    require(body == data['code'][552:1048] and compiled == build['compilerEvidence'] and compiled['generalCCompilerClaimed'] is False
        and compiled['initializationOnly'] is True and compiled['branchDecisionLogicClaimed'] is False, 'Complete496B source-only initializer product')
    stage = root / 'work/script-source/20261030/batch18/validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for name, copied in inputs.items():
            shutil.copyfile(copied, directory / name)
        subprocess.run(build['command'], cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        require((directory / 'generated.scrfunc').read_bytes() == body and json.loads((directory / 'build.json').read_text()) == compiled,
            'Fresh isolated source-only initializer rebuild')
    require(report['matchedRange'] == {'startPc': 552, 'endExclusivePc': 1048, 'bytes': 496, 'sha256': digest(body)}
        and checked(root, build['rebuiltImage']).read_bytes() == data['script'], 'Complete current initializer source range/image')
    require(len(report['compilerControls']) == 10, 'Ten source/type/storage controls')
    for row in report['compilerControls']:
        source, header = checked(root, row['source']), checked(root, row['header'])
        require(header == source.parent / 'scr_registered_globals.h', 'Control declaration closure')
        try:
            matcher.compiler.compile_source(source, 552, row['bindings'])
        except ValueError as error:
            require(str(error) == row['error'] and row['rejectedBeforeOutput'] is True, 'Actual source/type/storage rejection')
        else:
            raise ValueError('Invalid initializer source compiled')
    native_proof(report, matcher)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1 and report['qualifiedScriptRangeBytes'] == 496
        and report['originalScaffoldingBytes'] == len(data['script']) - 496 and report['initializationOnly'] is True
        and report['branchDecisionLogicClaimed'] is False, 'Single initialization-only definition/range')
    require(all(report[name] == 0 for name in ('scaffoldingSourceCredit', 'nativeExecutableByteCredit', 'completeImagesRecovered', 'nativeFunctionStubs'))
        and report['postFaultStateUsedForProof'] is False and report['wholeRomSourceMatch'] is False
        and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'Zero excess source/state/image credit')
    return {(digest(data['code']), 552): {'codeSha256': digest(data['code']), 'scriptSha256': data['scriptSha256'], 'asset': data['asset'],
        'startPc': 552, 'endExclusivePc': 1048, 'bytes': 496, 'sha256': digest(body), 'entryAliases': [256], 'mode': 'SCR', 'vmHostProcessor': 'ARM9',
        'source': 'src/scripts/20261030/batch18/clear_registered_keys.c', 'sourceSha256': compiled['sourceSha256'], 'sourceDefinitionCount': 1,
        'pairedCompleteOwnEntryExecutions': 128, 'pairedNativeReturningCalls': 3104, 'wholeImageReconstructed': False,
        'moduleGlobalSlots': list(range(3, 23)), 'privateLocalSlots': [], 'initializationOnly': True, 'branchDecisionLogicClaimed': False}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(row['bytes'] for row in units.values())}))
