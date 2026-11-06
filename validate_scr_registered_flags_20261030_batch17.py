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
SPEC = importlib.util.spec_from_file_location('_registered_flags_shared', SHARED)
shared = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_registered_flags_20261030_batch17.py'
MATCHER_HASH = '4e598094ada3d74c3a3ada59494b001a1a2d116b0d43f8eae93b046da412d023'
REPORT = 'evidence/matches/scripts-20261030-registered-flags.json'


def invocation(matcher, part, observed, profile, input_word, state, registers, instructions):
    native, f = matcher.fixtures.native, matcher.fixtures
    selected = next((index for index, raw in enumerate(profile['keys']) if f.floating(input_word) == f.floating(raw)), None)
    returned = input_word if selected is not None else f.fword(-1)
    index_word = profile['indices'][selected] if selected is not None else f.fword(-1)
    getter = None
    if f.floating(returned) != -1:
        value = f.floating(index_word)
        require(math.isfinite(value) and value == int(value) and 0 <= value <= 1535, 'Selected dynamic primary index qualification')
        index = int(value)
        previous = int(bool(state[native.PRIMARY + index // 8 - native.PERSIST] & (1 << (index & 7))))
        getter = {'index': index, 'previous': previous}
        if previous:
            index_word = f.fword(-1)
    require(part['inputWord'] == input_word and part['selectedKeySlot'] == selected and part['getter'] == getter
        and part['persistentBeforeHex'] == bytes(state).hex() and part['registerFileBeforeHex'] == bytes(registers).hex(),
        'Exact scalar/module selection/input/state carry')
    pc, args, condition = 7228, [input_word, 0], None
    trace, branches, actions, stores = [], [], [], []

    def operand(mode, raw):
        if mode == 0:
            return struct.unpack_from('<I', registers, int(f.floating(raw)) * 4)[0]
        if mode == 1:
            return args[int(f.floating(raw))]
        require(mode == 2, 'Qualified scalar operand mode')
        return raw

    for observation in observed:
        row = instructions[pc]
        op, raw = row['opcode'], row['argumentsRaw']
        following = pc + row['bytes']
        if op == 1036:
            following = raw[1]
        elif op in (1039, 1040):
            left, right = f.floating(operand(raw[1], raw[2])), f.floating(operand(raw[3], raw[4]))
            condition = left == right if op == 1039 else left != right
        elif op == 1038:
            require(condition is not None, 'Comparison dominates conditional branch')
            taken = not condition
            following = raw[1] if taken else following
            branches.append({'pc': pc, 'takenToEncodedTarget': taken})
        elif op == 1045:
            destination = int(f.floating(raw[2]))
            value = operand(raw[3], raw[4])
            if raw[1] == 0:
                require(destination in (42, 43, 44), 'Only three private local stores')
                struct.pack_into('<I', registers, destination * 4, value)
            else:
                require(raw[1] == 1 and destination in (0, 1), 'Only two API/result argument stores')
                args[destination] = value
        elif op in (41, 42):
            require(getter is not None and f.floating(args[0]) == getter['index'], 'Selected bounded actual primary API index')
            actions.append({'pc': pc, 'api': 'get_primary_flag' if op == 41 else 'set_primary_flag',
                'index': getter['index'], 'previous': getter['previous']})
            if op == 41:
                args[0] = f.fword(getter['previous'])
            else:
                require(f.floating(args[1]) == 1 and getter['previous'] == 0, 'False-to-true only supported setter effect')
                index = getter['index']
                native.bit_set(state, native.PRIMARY, index, True)
                address = native.PRIMARY + (index >> 5) * 4
                stores.append({'address': hex(address), 'bytes': 4, 'value': struct.unpack_from('<I', state, address - native.PERSIST)[0]})
        elif op == 1026:
            following = pc
        else:
            require(op == 1024, 'Supported complete registered-flag record')
        require(observation['entry'] == ('0x204c5a0' if op >= 1024 else '0x205a65c') and observation['resultWord'] == 1
            and observation['persistentSha256'] == digest(state), 'Actual return/full persistent effect at every record')
        trace.append({'pc': pc, 'opcode': op, 'nextPc': following})
        pc = following
    require(trace[-1]['pc'] == 8352 and trace[-1]['opcode'] == 1026 and part['completeEntryReturned'] is True and part['privateReturnPc'] == 8352,
        'Complete private scalar return')
    require(part['trace'] == trace and part['branches'] == branches and part['actions'] == actions, 'Every first-match/guard/flag branch and action')
    require(part['returnedScalarWord'] == returned == args[0] and part['finalFlagIndexWord'] == index_word
        and struct.unpack_from('<I', registers, 42 * 4)[0] == returned and struct.unpack_from('<I', registers, 43 * 4)[0] == index_word,
        'Raw scalar return/sentinel/index-local representation')
    require(part['orderedPrimaryWordStores'] == stores and part['persistentAfterSha256'] == digest(state)
        and part['registerFileAfterSha256'] == digest(registers) and part['allOtherSlotsIncludingModuleGlobalsPreserved'] is True,
        'Ordered aligned-word setter/neighbors/all module/global state')


def native_proof(matcher, report, data):
    proof, f = report['differential'], matcher.fixtures
    profiles = f.profiles()
    require(len(profiles) == 31 and len(proof['cases']) == proof['freshMachines'] == 124 and proof['providerCount'] == 0
        and proof['nativeInstructionCap'] == 20000 and proof['nativeTimeoutMicroseconds'] == 1000000 and proof['scriptStepCap'] == 100
        and proof['serializedCompleteCallsOnly'] is True and proof['dynamicIndexDomainQualifiedOnlyWhenUsed'] == [0, 1535]
        and proof['opaqueGlobalDomainProofClaimed'] is False and proof['naturalSceneOrRenewabilityMeaningProven'] is False,
        'Qualified bounded dynamic-index/global/context population')
    instructions = {row['pc']: row for row in data['instructions'] if 7228 <= row['pc'] < 8356}
    calls, records, branches = 0, set(), {}
    for ordinal, case in enumerate(proof['cases']):
        thread, profile, seed = ordinal // 31, profiles[ordinal % 31], 2026103027000 + ordinal
        require(case['profile'] == profile and (case['thread'], case['seed']) == (thread, seed), 'Independent registered-key scenario identity')
        state = bytearray(random.Random(seed).randbytes(0x7040))
        for raw in profile['indices']:
            index = f.floating(raw)
            if math.isfinite(index) and index == int(index) and 0 <= index <= 1535:
                f.native.bit_set(state, f.native.PRIMARY, int(index), profile['primaryEnabled'])
        registers = bytearray(random.Random(seed ^ 0xC17).randbytes(1024))
        for slot, raw in enumerate(profile['keys'] + profile['indices'], 3):
            struct.pack_into('<I', registers, slot * 4, raw)
        require(case['initialRegisterFileHex'] == registers.hex(), 'Explicit module-global bindings/random other slots')
        observed = case['observations']
        shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([row['entry'] for row in observed[:len(startup)]] == startup, 'Natural native start/forks')
        cursor = len(startup)
        for iteration, name in enumerate(('first', 'second')):
            if iteration:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0'), 'Natural serialized reentry')
                cursor += 1
            part = case[name]
            end = cursor + len(part['trace'])
            invocation(matcher, part, observed[cursor:end], profile, profile['inputs'][iteration], state, registers, instructions)
            cursor = end
            records.update(row['pc'] for row in part['trace'])
            for row in part['branches']:
                branches.setdefault(str(row['pc']), set()).add(row['takenToEncodedTarget'])
        require(cursor == len(observed) == case['actualReturningCalls'], 'Per-context actual native returns')
        calls += cursor
    require(all(values == {False, True} for values in branches.values()) and proof['branchCoverage'] ==
        {pc: sorted(values) for pc, values in branches.items()}, 'All twelve branch outcomes')
    require(proof['executedOwnRecordPcs'] == sorted(records) == report['boundariesAndStorage']['reachableOwnRecordPcs'], 'All own source records executed')
    require(proof['actualReturningCalls'] == calls == 7374 and report['pairedNativeReturningCalls'] == 14748
        and proof['completeEntryExecutions'] == 248 and report['pairedCompleteOwnEntryExecutions'] == 496, 'Separate complete-entry/native-return totals')


def controls(matcher, report):
    proof = report['compilerControls']
    require(len(proof['rejectedSourceProfiles']) == 10 and proof['controlSourceCredit'] == proof['nativeErrorPathCredit'] == 0
        and proof['generalModuleGlobalDomainProofClaimed'] is False, 'Explicit source/domain-control scope')
    for row in proof['rejectedSourceProfiles']:
        source = checked(ROOT, row['source'])
        require((source.parent / 'scr_registered_flags.h').read_bytes() == (matcher.SOURCE / 'scr_registered_flags.h').read_bytes(), 'Control ABI closure')
        try:
            matcher.compiler.compile_source(source, 7228, row['bindings'])
        except ValueError as error:
            require(str(error) == row['error'] and row['rejectedBeforeOutput'] is True, 'Actual source/type/domain rejection')
        else:
            raise ValueError('Unsupported registered-flag source compiled')
    require(len(proof['unsupportedDynamicIndexContexts']) == 5, 'Five explicit unsupported dynamic-index contexts')
    for case, raw in zip(proof['unsupportedDynamicIndexContexts'], (matcher.fixtures.fword(-1), matcher.fixtures.fword(1536),
            matcher.fixtures.fword(31.5), 0x7FC12345, 0x7F800000)):
        require(case['profile']['indices'][0] == raw and case['domainRejectedBeforeOwnEntryExecution'] is True
            and case['nativeErrorPathClaimed'] is False and case['completeEntryReturnCredit'] == case['postStopStateCredit'] == 0,
            'Unsupported contexts receive no native-error/return/state credit')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Local pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(row.value) for row in ast.parse(path.read_text()).body if isinstance(row, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'PINS' for target in row.targets))
    for name, pin in pins.items():
        checked(root, {'path': name, 'sha256': pin})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_registered_flags_matcher')
    for name, pin in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
            ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH), ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': pin})
    matcher.assets.original_files.cache_clear()
    data = matcher.assets.load(root / 'extract/files/world.e')
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['evidenceClass'] == 'ordinary-C-complete-registered-dynamic-primary-float-return-SCR-source-match'
        and report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH and report['sourceClosure'] ==
        [{'path': name, 'sha256': pin} for name, pin in pins.items()], 'Frozen scalar-return source/generator/closure')
    unused, files = matcher.assets.original_files()
    require(report['romSha256'] == matcher.assets.ROM_HASH and report['romFileRange'] == list(files['world.e'])
        and report['archiveSha256'] == data['assetSha256'] and report['scriptSha256'] == data['scriptSha256']
        and report['codeSha256'] == digest(data['code']), 'Current original ROM/image identity')
    require(report['boundariesAndStorage'] == matcher.boundary(data), 'Current full private/direct/local/module-global bounds')
    build = report['sourceOnlyBuild']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False and build['cwd'] ==
        str(root / 'work/script-source/20261030/batch17/registered-flags/source-only') and build['command'] ==
        [sys.executable, 'scr_c_compiler_20261030_v14.py', '--source', 'apply_registered_primary.c', '--base', hex(7228),
        '--bindings', 'registered.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json'], 'Actual source-only command/directory')
    inputs = {Path(row['path']).name: checked(root, row) for row in build['inputs']}
    require(len(inputs) == len(build['inputs']) == 5, 'Complete scalar-return source-only closure')
    for name, path in inputs.items():
        origin = name if name.endswith('.py') else 'src/scripts/20261030/batch17/' + name
        require(digest(path.read_bytes()) == pins[origin], 'Copied frozen source-only input')
    body = checked(root, build['emittedBody']).read_bytes()
    compiled = json.loads(checked(root, build['compilerReport']).read_text())
    require(body == data['code'][7228:8356] and compiled == build['compilerEvidence'] and compiled['generalCCompilerClaimed'] is False
        and compiled['opaqueGlobalDomainProofClaimed'] is False, 'Complete1128B scalar-return source-only product')
    stage = root / 'work/script-source/20261030/batch17/validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for name, path in inputs.items():
            shutil.copyfile(path, directory / name)
        subprocess.run(build['command'], cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        require((directory / 'generated.scrfunc').read_bytes() == body and json.loads((directory / 'build.json').read_text()) == compiled,
            'Fresh isolated scalar-return source rebuild')
    require(report['matchedRange'] == {'startPc': 7228, 'endExclusivePc': 8356, 'bytes': 1128, 'sha256': digest(body)}
        and checked(root, build['rebuiltImage']).read_bytes() == data['script'], 'Complete current source range/image')
    controls(matcher, report)
    native_proof(matcher, report, data)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1 and report['qualifiedScriptRangeBytes'] == 1128
        and report['originalScaffoldingBytes'] == len(data['script']) - 1128, 'One complete scalar-return source scope')
    require(all(report[name] == 0 for name in ('scaffoldingSourceCredit', 'nativeExecutableByteCredit', 'completeImagesRecovered', 'nativeFunctionStubs'))
        and report['postFaultStateUsedForProof'] is False and report['wholeRomSourceMatch'] is False
        and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'Zero excess/post-fault source credit')
    return {(digest(data['code']), 7228): {'codeSha256': digest(data['code']), 'scriptSha256': data['scriptSha256'], 'asset': data['asset'],
        'startPc': 7228, 'endExclusivePc': 8356, 'bytes': 1128, 'sha256': digest(body), 'entryAliases': [259], 'mode': 'SCR', 'vmHostProcessor': 'ARM9',
        'source': 'src/scripts/20261030/batch17/apply_registered_primary.c', 'sourceSha256': compiled['sourceSha256'], 'sourceDefinitionCount': 1,
        'pairedCompleteOwnEntryExecutions': 496, 'pairedNativeReturningCalls': 14748, 'wholeImageReconstructed': False,
        'moduleGlobalSlots': list(range(3, 23)), 'privateLocalSlots': [42, 43, 44], 'returnConvention': 'VM argument register0 raw binary32'}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(row['bytes'] for row in units.values())}))
