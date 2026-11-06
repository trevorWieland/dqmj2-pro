import ast
import importlib.util
import json
import random
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HELPER = ROOT / 'validate_scr_empty_family_20261029_batch04.py'
import hashlib
if hashlib.sha256(HELPER.read_bytes()).hexdigest() != 'c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604':
    raise ValueError('Frozen validation helper identity')
spec = importlib.util.spec_from_file_location('_numeric_validation_helpers', HELPER)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
require, digest, checked, local = helpers.require, helpers.digest, helpers.checked, helpers.local
MATCHER = 'match_scr_numeric_transition_20261029_batch04.py'
MATCHER_HASH = '95d85c5e1223872be29b98263d75965e5310b987b0338541b37af790a4292b4f'
REPORT = 'evidence/matches/scripts-20261029-numeric-transition.json'
BASE, END = 64612, 64964


def word(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def observations(items):
    for item in items:
        require(item['actualReturn'] is True and 0 < item['instructions'] <= 20000, 'Actual bounded native return')
        for key in ('registersSha256', 'orderedCpuStoresSha256', 'vmContextSha256',
                    'globalVmContextSha256', 'persistentSha256'):
            require(re.fullmatch('[0-9a-f]{64}', item[key]) is not None, 'Native state digest')


def invocation(part, context_word, zero, nine, before):
    context = struct.unpack('<f', struct.pack('<I', context_word))[0]
    branches = [context == 60]
    if branches[0]:
        branches.append(zero == 7)
        if branches[1]:
            branches.append(nine == 2)
    success = all(branches) and len(branches) == 3
    after = bytearray(before)
    if success:
        after[0x021C0DC8 + 9 - 0x021B9EB4] = 3
    offsets = [0, 12, 36, 60, 68, 92, 116, 124, 148, 172]
    if branches[0]:
        offsets += [184, 208]
        if branches[1]:
            offsets += [220, 244]
            if branches[2]:
                offsets += [256, 280, 304, 312]
            offsets += [324]
        offsets += [336]
    offsets += [348]
    opcodes = {0: 1036, 12: 1045, 36: 1045, 60: 39, 68: 1045, 92: 1045, 116: 39,
               124: 1045, 148: 1039, 172: 1038, 184: 1039, 208: 1038, 220: 1039,
               244: 1038, 256: 1045, 280: 1045, 304: 40, 312: 1036, 324: 1036, 336: 1036, 348: 1026}
    trace = [{'pc': BASE + offset, 'opcode': opcodes[offset],
              'nextPc': BASE + (offsets[index + 1] if index + 1 < len(offsets) else offset)}
             for index, offset in enumerate(offsets)]
    require(part['trace'] == trace and part['completeFunctionTerminated'] is True, 'Full nested control flow/private RET')
    require(part['contextWord'] == context_word and part['initialNumericZero'] == zero
            and part['initialNumericNine'] == nine, 'Invocation input ABI')
    require(part['branchOutcomes'] == branches and part['numericNineChangedToThree'] == success, 'Measured predicate outcome')
    require(part['setterCalls'] == int(success), 'Conditional setter count')
    writes = [{'address': '0x21c0dd1', 'bytes': 1, 'value': 3}] if success else []
    require(part['targetByteWrites'] == writes, 'Exact persistent-byte writes')
    require(part['expectedPersistentSha256'] == digest(after), 'Independent expected persistent state')
    return bytes(after), trace


def differential(report):
    proof = report['differential']
    require(proof['instructionCapPerNativeCall'] == 20000 and proof['timeoutMicrosecondsPerNativeCall'] == 1000000,
            'Native execution bounds')
    require(proof['scriptStepBound'] == 24 and proof['serializedCompleteCallsOnly'] is True, 'Invocation scope')
    require(proof['naturalGameProducerOfContextValue60Proven'] is False, 'Natural reachability scope')
    inputs = [(word(c), z, n, t) for c in (59, 60) for z in (6, 7) for n in (1, 2)
              for t in range(4) for unused in range(2)]
    for context_word in (0, 0x80000000, word(61), word(60) - 1, word(60) + 1,
                         0x7F800000, 0xFF800000, 0x7FC00001, 0xFFC00001, word(16777216)):
        inputs += [(context_word, 7, 2, t) for t in range(4)]
    inputs += [(word(60), z, n, t) for z, n in ((0, 2), (255, 2), (7, 0), (7, 255), (0, 0), (255, 255))
               for t in range(4)]
    require(len(proof['cases']) == len(inputs) == 128, 'All branch/thread/byte/NaN cases')
    calls = 0
    for index, (case, (context_word, zero, nine, thread)) in enumerate(zip(proof['cases'], inputs)):
        seed = 2026103023001 + index
        require(case['seed'] == seed and case['thread'] == thread and case['contextInputProvidedExplicitly'] is True, 'Fixture identity')
        state = bytearray(random.Random(seed).randbytes(0x7040))
        state[0x021C0DC8 - 0x021B9EB4] = zero
        state[0x021C0DC8 + 9 - 0x021B9EB4] = nine
        initial_hash = digest(state)
        after, first = invocation(case['first'], context_word, zero, nine, state)
        final, second = invocation(case['second'], context_word, zero, after[0x021C0DC8 + 9 - 0x021B9EB4], after)
        require(case['second']['setterCalls'] == 0 and case['repeatedTransitionDoesNotRepeatWrite'] is True, 'Reentry state semantics')
        expected_entries = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        expected_entries += ['0x205a65c' if row['opcode'] < 1024 else '0x204c5a0' for row in first]
        first_end = len(expected_entries) - 1
        expected_entries += ['0x204bd00' if thread == 0 else '0x204bed0']
        expected_entries += ['0x205a65c' if row['opcode'] < 1024 else '0x204c5a0' for row in second]
        items = case['observations']
        require([item['entry'] for item in items] == expected_entries, 'Native ABI call order')
        require(case['actualReturningCalls'] == len(items), 'Actual returning call accounting')
        observations(items)
        require(items[0]['persistentSha256'] == initial_hash and items[first_end]['persistentSha256'] == digest(after)
                and items[-1]['persistentSha256'] == digest(final), 'Captured boundary states')
        calls += len(items)
    errors = proof['supportedErrors']
    require(len(errors) == 1 and errors[0]['kind'] == 'native-rejected-negative-entry'
            and errors[0]['ownedFunctionExecuted'] is False and errors[0]['actualReturningCalls'] == 2, 'Supported error path')
    observations(errors[0]['observations'])
    require([item['entry'] for item in errors[0]['observations']] == ['0x204bc08', '0x204bd00']
            and [item['resultWord'] for item in errors[0]['observations']] == [1, 0], 'Error ABI results')
    calls += 2
    require(calls == proof['actualReturningCalls'] == report['actualReturningCallsPerImplementation'] == 3906,
            'Complete native call population')
    require(report['actualReturningCallsTotal'] == calls * 2 and proof['freshMachines'] == report['freshMachinesPerImplementation'] == 129,
            'Paired native call/machine totals')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(sys.version_info[:3] == (3, 13, 5), 'Pinned Python version')
    matcher_path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(node.value) for node in ast.parse(matcher_path.read_text()).body
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in node.targets))
    for name, sha in pins.items():
        checked(root, {'path': name, 'sha256': sha})
    sys.path.insert(0, str(root))
    matcher = helpers.load_module(matcher_path, '_numeric_frozen_matcher')
    require(matcher.ROOT == root and matcher.assets.ROOT == root and matcher.fixtures.native.ROOT == root,
            'Repository-local imported evidence dependencies')
    for name, expected in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
                           ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH),
                           ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': expected})
    matcher.assets.original_files.cache_clear()
    for image, expected in ((matcher.fixtures.native.MAIN, matcher.fixtures.native.MAIN_HASH),
                            (matcher.fixtures.native.OVERLAY, matcher.fixtures.native.OVERLAY_HASH),
                            (matcher.fixtures.native.ITCM, matcher.fixtures.native.ITCM_HASH)):
        require(digest(image) == expected, 'Current native module bytes')
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH, 'Evidence generator identity')
    require(report['sourceClosure'] == [{'path': name, 'sha256': sha} for name, sha in pins.items()], 'Source/tool/fixture closure')
    data, members = matcher.input_image()
    require(report['asset'] == data['asset'] and report['archiveSha256'] == data['assetSha256']
            and report['scriptSha256'] == data['scriptSha256'] and report['codeSha256'] == digest(data['code']), 'Current image hashes')
    require(report['members'] == members, 'Archive member aliases')
    rom, files = matcher.assets.original_files()
    interval = files['s07e01.e']
    require(report['romSha256'] == matcher.assets.ROM_HASH and report['romFileRange'] == list(interval), 'Pinned original ROM')
    require((root / data['asset']).read_bytes() == rom[interval[0]:interval[1]], 'ROM-backed archive allocation')
    profile = json.loads((root / 'src/scripts/20261029/batch04/numeric_nine.locals.json').read_text())
    boundary = json.loads(json.dumps(matcher.boundaries_and_slots(data, profile)))
    require(report['boundariesAndLocalStorage'] == boundary, 'Current direct/private boundaries and complete slot qualification')
    require(report['namedRuntimeApiLinks'] == matcher.named_links(), 'Named native API bindings')
    build = report['buildCommand']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False, 'Source-only command')
    inputs = {Path(item['path']).name: checked(root, item) for item in build['sourceOnlyInputClosure']}
    aliases = {'compiler_v4.py': 'scr_c_compiler_20261029_v4.py'}
    expected = {'scr_c_compiler_20261029.py', 'compiler_v4.py', 'advance_numeric_nine.c', 'scr_numeric.h', 'numeric_nine.locals.json'}
    require(set(inputs) == expected and len(build['sourceOnlyInputClosure']) == 5, 'Exact source-only closure')
    for name, path in inputs.items():
        source = aliases.get(name, name if name.endswith('.py') else 'src/scripts/20261029/batch04/' + name)
        require(digest(path.read_bytes()) == pins[source], 'Copied compiler/source/profile identity')
    directory = inputs['advance_numeric_nine.c'].parent
    body = (directory / 'generated.scrfunc').read_bytes()
    source_report = json.loads((directory / 'build.json').read_text())
    require(source_report == report['sourceOnlyBuild'], 'Current compiler report product')
    require(body == data['code'][BASE:END] and len(body) == 352, 'Current emitted source-only artifact')
    require(report['matchedRange'] == {'startPc': BASE, 'endExclusivePc': END, 'bytes': 352, 'sha256': digest(body)}, 'Qualified complete range')
    stage = root / 'work/script-source/20261029/batch04/numeric-validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        fresh_directory = Path(temporary)
        for name, path in inputs.items():
            shutil.copyfile(path, fresh_directory / name)
        command = [sys.executable, 'compiler_v4.py', '--source', 'advance_numeric_nine.c', '--base', hex(BASE),
                   '--locals', 'numeric_nine.locals.json', '--output', 'fresh.scrfunc', '--report', 'fresh.json']
        subprocess.run(command, cwd=fresh_directory, capture_output=True, text=True, timeout=30, check=True)
        require((fresh_directory / 'fresh.scrfunc').read_bytes() == body, 'Fresh source-only re-emission')
        fresh_report = json.loads((fresh_directory / 'fresh.json').read_text())
    for key in ('sourceSha256', 'includeSha256', 'compilerSha256', 'function', 'functionBase',
                'namedAllocationProfile', 'variableAllocations', 'namedApiCalls', 'generatedBranches', 'parsedAst', 'outputBytes', 'outputSha256'):
        require(fresh_report[key] == source_report[key], 'Compiler evidence field: ' + key)
    rebuilt = checked(root, report['rebuiltDecodedImage']).read_bytes()
    require(rebuilt == data['script'] and report['rebuiltDecodedImageEqualsOriginal'] is True, 'Current rebuilt decoded image')
    require(report['originalScaffoldingBytes'] == len(rebuilt) - 352, 'Scaffolding accounting')
    for key in ('scaffoldingSourceCredit', 'completeImagesRecovered', 'ordinaryNativeExecutableByteCredit', 'nativeFunctionStubs'):
        require(report[key] == 0, 'Evidence credit scope: ' + key)
    require(report['postFaultStateUsedForProof'] is False and report['allNestedBranchOutcomesTested'] is True
            and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'Proof scope')
    controls = report['compilerControls']
    require(len(controls['negativeSourcesOrProfiles']) == 18, 'Negative source/profile population')
    for item in controls['negativeSourcesOrProfiles']:
        path = checked(root, item['source'])
        require(item['rejectedBeforeOutput'] is True, 'Source rejection record')
        try:
            matcher.compiler.compile_source(path, BASE, item['profile'])
        except ValueError as error:
            require(str(error) == item['error'], 'Fresh source rejection reason')
        else:
            raise ValueError('Negative source/profile now compiles')
    require(controls['wrongNamedAllocationDoesNotMatchOriginal'] is True and controls['failedCliPreservesExistingOutputAndReport'] is True
            and controls['failedCliExitCode'] != 0 and controls['controlSourceCredit'] == 0, 'Compiler control scope')
    checked(root, controls['syntheticNumericElseSource'])
    positive = controls['syntheticNumericElseNativeCases']
    require([item['initialNumericNine'] for item in positive] == [0, 2, 3, 255], 'Generated if/else ABI cases')
    for item in positive:
        require(item['finalNumericNine'] == (3 if item['initialNumericNine'] == 2 else 2)
                and item['actualReturningCalls'] == len(item['trace']) + 2 and item['originalSourceCredit'] == 0,
                'Generated branch behavior')
    differential(report)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1
            and report['qualifiedScriptRangeBytes'] == 352, 'Source unit accounting')
    key = digest(data['code']), BASE
    return {key: {'codeSha256': key[0], 'scriptSha256': data['scriptSha256'], 'asset': data['asset'],
        'startPc': BASE, 'endExclusivePc': END, 'bytes': 352, 'sha256': digest(body), 'entryAliases': [102],
        'mode': 'SCR', 'vmHostProcessor': 'ARM9', 'source': 'src/scripts/20261029/batch04/advance_numeric_nine.c',
        'sourceSha256': source_report['sourceSha256'], 'sourceDefinitionCount': 1,
        'substantiveDecisionLogicBytes': 352, 'actualReturningCallsTotal': 7812, 'wholeImageReconstructed': False}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'qualifiedBytes': sum(item['bytes'] for item in units.values())}))
