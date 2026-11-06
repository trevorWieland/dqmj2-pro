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
    raise ValueError('Frozen shared numeric validator')
spec = importlib.util.spec_from_file_location('_primary24_shared', SHARED)
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_primary24_20261029_batch05.py'
MATCHER_HASH = '1672c50414bc5b8b0fba6dd3c5eefd41b8ba4be5de53fe987e4e2a05db833aed'
REPORT = 'evidence/matches/scripts-20261029-primary24.json'
BASE, END = 75216, 75568
PERSIST, NUMERIC, PRIMARY = 0x021B9EB4, 0x021C0DC8, 0x021C0E20


def word(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def invocation(part, context_word, zero, three, before):
    context = struct.unpack('<f', struct.pack('<I', context_word))[0]
    branches = [context == 12]
    if branches[0]:
        branches.append(zero == 2)
        if branches[1]:
            branches.append(three == 1)
    success = len(branches) == 3 and all(branches)
    after = bytearray(before)
    if success:
        after[PRIMARY + 3 - PERSIST] |= 1
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
        124: 1045, 148: 1039, 172: 1038, 184: 1039, 208: 1038, 220: 1039, 244: 1038,
        256: 1045, 280: 1045, 304: 42, 312: 1036, 324: 1036, 336: 1036, 348: 1026}
    trace = [{'pc': BASE + offset, 'opcode': opcodes[offset],
              'nextPc': BASE + (offsets[i + 1] if i + 1 < len(offsets) else offset)} for i, offset in enumerate(offsets)]
    require(part['trace'] == trace and part['completeFunctionTerminated'] is True, 'Complete branch/private return')
    require(part['contextWord'] == context_word and part['numericZero'] == zero and part['numericThree'] == three,
            'Typed input values')
    require(part['branchOutcomes'] == branches and part['setterCalls'] == int(success), 'Nested predicate outcome')
    store_word = struct.unpack_from('<I', after, PRIMARY - PERSIST)[0]
    writes = [{'address': hex(PRIMARY), 'bytes': 4, 'value': store_word}] if success else []
    require(part['targetByteWrites'] == writes, 'Exact32-bit primary word RMW')
    require(part['persistentChanged'] == (before != bytes(after)) and part['expectedPersistentSha256'] == digest(after),
            'Independent persistent effect')
    return bytes(after), trace


def native_proof(report):
    proof = report['differential']
    require(proof['instructionCapPerNativeCall'] == 20000 and proof['timeoutMicrosecondsPerNativeCall'] == 1000000
            and proof['scriptStepBound'] == 24 and proof['serializedCompleteCallsOnly'] is True, 'Execution bounds/scope')
    require(proof['naturalProducerOfContextTwelveProven'] is False, 'Unproved natural input scope')
    inputs = [(word(c), z, t, flag, thread) for c in (11, 12) for z in (1, 2) for t in (0, 1)
              for flag in (False, True) for thread in range(4)]
    for context_word in (0, 0x80000000, word(13), word(12) - 1, word(12) + 1,
                         0x7F800000, 0xFF800000, 0x7FC00001, 0xFFC00001, word(16777216)):
        inputs += [(context_word, 2, 1, False, thread) for thread in range(4)]
    inputs += [(word(12), z, t, False, thread) for z, t in ((0, 1), (255, 1), (2, 0), (2, 255), (0, 0), (255, 255))
               for thread in range(4)]
    require(len(proof['cases']) == len(inputs) == 128, 'Complete input/branch/thread population')
    calls = 0
    for index, (case, (context_word, zero, three, flag, thread)) in enumerate(zip(proof['cases'], inputs)):
        seed = 2026103032001 + index
        require(case['seed'] == seed and case['thread'] == thread and case['initialPrimary24'] == flag
                and case['contextInputProvidedExplicitly'] is True, 'Scenario identity')
        initial = bytearray(random.Random(seed).randbytes(0x7040))
        initial[NUMERIC - PERSIST], initial[NUMERIC + 3 - PERSIST] = zero, three
        initial[PRIMARY + 3 - PERSIST] = (initial[PRIMARY + 3 - PERSIST] | 1) if flag else (initial[PRIMARY + 3 - PERSIST] & 254)
        after, first = invocation(case['first'], context_word, zero, three, initial)
        final, second = invocation(case['second'], context_word, zero, three, after)
        require(case['second']['setterCalls'] == case['first']['setterCalls'] and case['second']['persistentChanged'] is False
                and case['reentryMayRepeatSetterButNotPersistentChange'] is True, 'Repeated setter/word-store semantics')
        entries = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        entries += ['0x205a65c' if row['opcode'] < 1024 else '0x204c5a0' for row in first]
        first_end = len(entries) - 1
        entries += ['0x204bd00' if thread == 0 else '0x204bed0']
        entries += ['0x205a65c' if row['opcode'] < 1024 else '0x204c5a0' for row in second]
        observations = case['observations']
        shared.observations(observations)
        require([item['entry'] for item in observations] == entries
                and len(observations) == case['actualReturningCalls'], 'Exact native return population/order')
        require(observations[0]['persistentSha256'] == digest(initial)
                and observations[first_end]['persistentSha256'] == digest(after)
                and observations[-1]['persistentSha256'] == digest(final), 'Captured persistent boundaries')
        calls += len(observations)
    errors = proof['supportedErrors']
    require(len(errors) == 1 and errors[0]['kind'] == 'native-rejected-negative-entry'
            and errors[0]['ownedFunctionExecuted'] is False and errors[0]['actualReturningCalls'] == 2, 'Supported error path')
    shared.observations(errors[0]['observations'])
    require([item['entry'] for item in errors[0]['observations']] == ['0x204bc08', '0x204bd00']
            and [item['resultWord'] for item in errors[0]['observations']] == [1, 0], 'Negative entry results')
    calls += 2
    prefixes = proof['outsideReaderInitializationPrefixes']
    require(len(prefixes) == 3, 'All outside-reader prefix controls')
    pcs = [73888, 73900, 73924, 73932, 73956, 73964, 73988, 74012, 74020, 74044, 74068, 74076]
    ops = [1036, 1045, 47, 1045, 48, 1045, 1045, 39, 1045, 1045, 39, 1045]
    for index, (prefix, (zero, three)) in enumerate(zip(prefixes, ((0, 0), (2, 1), (255, 255)))):
        seed = 2026103033000 + index
        require(prefix['seed'] == seed and prefix['numericZero'] == zero and prefix['numericThree'] == three, 'Prefix inputs')
        require(prefix['ownerRoutineTerminated'] is False and prefix['boundaryCountedAsReturn'] is False
                and prefix['boundaryPc'] == 74100 and prefix['sourceCredit'] == 0, 'Prefix is not outer termination/source credit')
        trace = [{'pc': pc, 'opcode': op, 'nextPc': pcs[i + 1] if i + 1 < len(pcs) else 74100}
                 for i, (pc, op) in enumerate(zip(pcs, ops))]
        require(prefix['trace'] == trace and prefix['slot138Word'] == word(zero)
                and prefix['slot139Word'] == word(three), 'Outside-reader unconditional initialization')
        observed = prefix['observations']
        shared.observations(observed)
        require(len(observed) == prefix['actualReturningCalls'] == 14, 'True prefix native returns')
        require([row['entry'] for row in observed] == ['0x204bc08', '0x204bd00'] +
                ['0x205a65c' if op < 1024 else '0x204c5a0' for op in ops], 'Prefix native API order')
        initial = bytearray(random.Random(seed).randbytes(0x7040))
        initial[NUMERIC - PERSIST], initial[NUMERIC + 3 - PERSIST] = zero, three
        require(all(row['persistentSha256'] == digest(initial) for row in observed), 'Prefix persistent preservation')
        calls += 14
    require(calls == proof['actualReturningCalls'] == report['actualReturningCallsPerImplementation'] == 3980
            and report['actualReturningCallsTotal'] == 7960, 'Paired native call totals')
    require(proof['freshMachines'] == report['freshMachinesPerImplementation'] == 132, 'Machine totals')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(sys.version_info[:3] == (3, 13, 5), 'Pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(node.value) for node in ast.parse(path.read_text()).body
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in node.targets))
    for name, sha in pins.items():
        checked(root, {'path': name, 'sha256': sha})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_primary24_frozen_matcher')
    require(matcher.ROOT == matcher.assets.ROOT == matcher.fixtures.native.ROOT == root, 'Repository-local imports')
    matcher.assets.original_files.cache_clear()
    for name, sha in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
                      ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH),
                      ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': sha})
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH
            and report['sourceClosure'] == [{'path': name, 'sha256': sha} for name, sha in pins.items()], 'Frozen generator/closure')
    data = matcher.assets.load(root / 'extract/files/s02e10.e')
    rom, files = matcher.assets.original_files()
    interval = files['s02e10.e']
    require(report['romSha256'] == matcher.assets.ROM_HASH and report['romFileRange'] == list(interval), 'ROM hash/interval')
    raw = (root / data['asset']).read_bytes()
    require(raw == rom[interval[0]:interval[1]] and report['archiveSha256'] == data['assetSha256']
            and report['scriptSha256'] == data['scriptSha256'] and report['codeSha256'] == digest(data['code']), 'Current archive/image')
    members = []
    for index in range(matcher.assets.u32(raw, 4)):
        offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
        stored = raw[offset:offset + length]
        require(matcher.assets.ash(stored) == data['script'], 'Decoded member alias')
        members.append({'index': index, 'storedOffset': offset, 'storedBytes': length,
                        'storedSha256': digest(stored), 'scriptSha256': data['scriptSha256']})
    require(report['members'] == members, 'Complete archive alias population')
    profile = json.loads((root / 'src/scripts/20261029/batch05/primary24.locals.json').read_text())
    require(report['boundariesAndLocalStorage'] == json.loads(json.dumps(matcher.boundaries(data, profile))),
            'Full direct/private bounds and outside-read dominance')
    require(report['namedRuntimeApiLinks'] == matcher.named_links(), 'Native API identities')
    build = report['buildCommand']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False, 'Source-only compiler command')
    inputs = {Path(item['path']).name: checked(root, item) for item in build['sourceOnlyInputClosure']}
    expected = {'scr_c_compiler_20261029.py', 'compiler_v4.py', 'set_primary_24.c', 'scr_numeric.h', 'primary24.locals.json'}
    require(set(inputs) == expected and len(build['sourceOnlyInputClosure']) == 5, 'Exact source-only inputs')
    for name, item in inputs.items():
        original = 'scr_c_compiler_20261029_v4.py' if name == 'compiler_v4.py' else name if name.endswith('.py') else 'src/scripts/20261029/batch05/' + name
        require(digest(item.read_bytes()) == pins[original], 'Compiler/source/profile copied identity')
    body = checked(root, build['emittedBody']).read_bytes()
    source_report = json.loads(checked(root, build['compilerReport']).read_text())
    require(source_report == report['sourceOnlyBuild'] and body == data['code'][BASE:END], 'Current emitted body/compiler report')
    require(report['matchedRange'] == {'startPc': BASE, 'endExclusivePc': END, 'bytes': 352, 'sha256': digest(body)}, 'Complete352B gate')
    stage = root / 'work/script-source/20261029/batch05/primary24-validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for name, item in inputs.items():
            shutil.copyfile(item, directory / name)
        command = [sys.executable, 'compiler_v4.py', '--source', 'set_primary_24.c', '--base', hex(BASE),
                   '--locals', 'primary24.locals.json', '--output', 'fresh.scrfunc', '--report', 'fresh.json']
        subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        require((directory / 'fresh.scrfunc').read_bytes() == body, 'Fresh source-only re-emission')
        fresh = json.loads((directory / 'fresh.json').read_text())
    for key in ('sourceSha256', 'includeSha256', 'compilerSha256', 'function', 'functionBase', 'namedAllocationProfile',
                'variableAllocations', 'namedApiCalls', 'generatedBranches', 'parsedAst', 'outputBytes', 'outputSha256'):
        require(fresh[key] == source_report[key], 'Compiler evidence: ' + key)
    require(checked(root, report['rebuiltDecodedImage']).read_bytes() == data['script']
            and report['rebuiltDecodedImageEqualsOriginal'] is True, 'Rebuilt decoded image')
    require(report['originalScaffoldingBytes'] == len(data['script']) - 352, 'Scaffolding size')
    for key in ('scaffoldingSourceCredit', 'completeImagesRecovered', 'ordinaryNativeExecutableByteCredit', 'nativeFunctionStubs'):
        require(report[key] == 0, 'Credit scope: ' + key)
    require(report['postFaultStateUsedForProof'] is False
            and report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True, 'Native proof scope')
    controls = report['compilerControls']
    require(len(controls['rejectedSourceProfiles']) == 10 and controls['wrongValidAllocationChangesBytes'] is True
            and controls['sourceCredit'] == 0, 'Source/profile controls')
    for item in controls['rejectedSourceProfiles']:
        source = checked(root, item['source'])
        try:
            matcher.compiler.compile_source(source, BASE, item['profile'])
        except ValueError as error:
            require(str(error) == item['error'] and item['rejectedBeforeOutput'] is True, 'Current rejection reason')
        else:
            raise ValueError('Negative source/profile now compiles')
    native_proof(report)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1
            and report['qualifiedScriptRangeBytes'] == 352, 'Qualified unit population')
    key = digest(data['code']), BASE
    return {key: {'codeSha256': key[0], 'scriptSha256': data['scriptSha256'], 'asset': data['asset'],
        'startPc': BASE, 'endExclusivePc': END, 'bytes': 352, 'sha256': digest(body), 'mode': 'SCR',
        'vmHostProcessor': 'ARM9', 'entryAliases': [102], 'source': 'src/scripts/20261029/batch05/set_primary_24.c',
        'sourceSha256': source_report['sourceSha256'], 'sourceDefinitionCount': 1, 'substantiveDecisionLogicBytes': 352,
        'actualReturningCallsTotal': 7960, 'outsideReadPrefixSourceCredit': 0, 'wholeImageReconstructed': False}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(unit['bytes'] for unit in units.values())}))
