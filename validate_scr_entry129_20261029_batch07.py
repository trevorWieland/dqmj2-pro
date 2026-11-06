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
    raise ValueError('Frozen numeric validation helper')
spec = importlib.util.spec_from_file_location('_entry129_validation_helpers', SHARED)
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
require, checked, digest, local = shared.require, shared.checked, shared.digest, shared.local
MATCHER = 'match_scr_entry129_20261029_batch07.py'
MATCHER_HASH = '9c5d390f23db80912210f446e949d7f8e50c1e0e56bbc46118bf54d12075e8c3'
REPORT = 'evidence/matches/scripts-20261029-entry129.json'
BASE, END, PERSIST, NUMERIC, PRIMARY = 137336, 138096, 0x021B9EB4, 0x021C0DC8, 0x021C0E20


def word(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def invocation(proof, raw, status, initial_flag, records):
    require(proof['rawContextByte'] == raw and proof['engineState'] == status
            and proof['completeEntry129Returned'] is True and proof['finalPc'] == END - 4, 'Whole entry return/input')
    flag = initial_flag if status == 57 and raw == 59 else None
    require(proof['sourceFlag222'] == flag, 'Observed caller primary222 predicate')
    decisions = [(137476, status == 57)]
    if status == 57:
        decisions.append((137512, raw == 59))
        if raw == 59:
            decisions.append((137604, not flag))
    else:
        decisions.append((137752, raw == 66))
    require(proof['ownBranches'] == [{'pc': pc, 'decision': value} for pc, value in decisions], 'Every caller branch decision')
    expected_calls = [{'name': 'advance_numeric_nine_when_values_match', 'callPc': 137404, 'targetPc': 64612,
                      'expectedReturnPc': 137416, 'argumentCount': 0},
                     {'name': 'process_imported_context', 'callPc': 137440, 'targetPc': 138616,
                      'expectedReturnPc': 137452, 'argumentCount': 1, 'argumentWord': word(raw)}]
    require(proof['namedCalls'] == expected_calls, 'Qualified declared original call ABI')
    trace, stack, expected_pc = proof['trace'], [], BASE
    branch_map = dict(decisions)
    for index, step in enumerate(trace):
        pc, opcode = step['pc'], step['opcode']
        require(pc == expected_pc and opcode == records[pc]['opcode'] and step['ownBody'] == (BASE <= pc < END), 'Current full trace body identity')
        row = records[pc]
        if opcode == 1033:
            stack.append(pc + row['bytes'])
            target = row['argumentsRaw'][1]
        elif opcode == 1026:
            target = stack.pop() if stack else pc
            if target == pc:
                require(index == len(trace) - 1 and pc == END - 4, 'Caller private RET is final termination')
        elif opcode == 1036:
            target = row['argumentsRaw'][1]
        elif opcode == 1038:
            if pc in branch_map:
                target = pc + row['bytes'] if branch_map[pc] else row['argumentsRaw'][1]
            else:
                require(step['nextPc'] in (pc + row['bytes'], row['argumentsRaw'][1]), 'Original callee conditional edge')
                target = step['nextPc']
        else:
            target = pc + row['bytes']
        require(step['nextPc'] == target and step['depthAfter'] == len(stack), 'Real CALL/RET stack and exact continuation')
        expected_pc = target
    require(trace and not stack and trace[-1]['pc'] == END - 4 and trace[-1]['opcode'] == 1026, 'Entire caller completed')
    actions = proof['ownActions']
    if status == 57 and raw == 59 and not flag:
        require(len(actions) == 1 and actions[0]['pc'] == 137664 and actions[0]['opcode'] == 42
                and actions[0]['arguments'] == [262.0, 1.0], 'Caller primary262 write')
    elif status != 57 and raw == 66:
        require([action['opcode'] for action in actions] == [261, 40, 40, 266, 98], 'Entire native request branch')
        require(actions[0] == {'pc': 137788, 'opcode': 261, 'identifier': 130}, 'Measured request selector')
        require([(action['pc'], action['arguments']) for action in actions[1:3]] ==
                [(137844, [50.0, 0.0]), (137900, [51.0, 4.0])], 'Numeric50/51 assignments')
        require(actions[3] == {'pc': 137932, 'opcode': 266, 'argument': 90, 'storedWords': [0xFFFA6000, 0xFFFA6000]}, 'Measured request scalar words')
        require(actions[4] == {'pc': 138060, 'opcode': 98,
            'argumentWords': [word(130), word(-38.97), 0, 0, word(90)], 'pendingIdentifier': 130, 'newRawByte': 130}, 'Raw float bits and request submission')
        require(proof['pendingRawByte'] == 130, 'Pending raw input differs from retained VM input')
    else:
        require(not actions, 'No unsupported caller-side action')
    return decisions


def native_proof(report, data):
    proof = report['differential']
    require(proof['nativeInstructionCap'] == 20000 and proof['nativeTimeoutMicroseconds'] == 1000000
            and proof['scriptStepBound'] == 1500 and proof['serializedCompleteCallsOnly'] is True, 'Native execution bounds')
    require(proof['originalDelegatedHelperSourceCredit'] == 0 and proof['priorHighControlFieldBoundProbePreserved'] is True, 'Original callee/bound scope')
    inputs = [(59, 57, 7, 2, f222, f262, thread) for f222 in (False, True) for f262 in (False, True) for thread in range(4)]
    inputs += [(60, 0, zero, nine, False, False, thread) for zero in (6, 7) for nine in (1, 2) for thread in range(4)]
    inputs += [(raw, status, 7, 2, False, False, thread) for raw, status in
               ((66, 0), (66, 57), (61, 0), (59, 0), (60, 57), (0, 0), (255, 57)) for thread in range(4)]
    require(len(inputs) == len(proof['cases']) == 60, 'All supported input/branch/thread/reentry scenarios')
    records = {row['pc']: row for row in data['instructions']}
    calls, coverage = 0, {pc: set() for pc in (137476, 137512, 137604, 137752)}
    for index, (case, values) in enumerate(zip(proof['cases'], inputs)):
        raw, status, zero, nine, f222, f262, thread = values
        seed = 2026103042001 + index
        require(case['seed'] == seed and case['thread'] == thread and case['initialInputs'] == {
            'raw': raw, 'status': status, 'numericZero': zero, 'numericNine': nine, 'primary222': f222, 'primary262': f262}, 'Native fixture identity')
        require(case['explicitSyntheticControlHalfword'] == {'ram': '0x021c0ecc', 'value': 0, 'semanticMeaningProven': False}, 'Explicit unknown-control synthetic0 prerequisite')
        require(case['reentryUsesSameVmContextBankNotRelauncherImport'] is True, 'Reentry contract')
        initial = bytearray(random.Random(seed).randbytes(0x7040))
        initial[NUMERIC - PERSIST], initial[NUMERIC + 9 - PERSIST] = zero, nine
        struct.pack_into('<H', initial, 0x021C0ECC - PERSIST, 0)
        for flag, enabled in ((222, f222), (262, f262)):
            position, bit = PRIMARY + flag // 8 - PERSIST, 1 << (flag & 7)
            initial[position] = initial[position] | bit if enabled else initial[position] & ~bit
        observations = case['observations']
        shared.observations(observations)
        require(observations[0]['persistentSha256'] == digest(initial), 'Independently seeded initial state')
        entries = ['0x204bc08', '0x205bdfc', '0x21e4e9c'] + ['0x204bed0'] * thread
        first_start = len(entries)
        for name in ('first', 'second'):
            item = case[name]
            for pc, value in invocation(item, raw, status, f222, records):
                coverage[pc].add(value)
            start = len(entries)
            entries += ['0x205a65c' if step['opcode'] < 1024 else '0x204c5a0' for step in item['trace']]
            require(observations[len(entries) - 1]['persistentSha256'] == item['finalPersistentSha256'], 'Whole entry final state')
            for action in item['ownActions']:
                if 'beforeSha256' in action:
                    offset = next(i for i, step in enumerate(item['trace']) if step['pc'] == action['pc'])
                    observed_index = start + offset
                    require(observations[observed_index - 1]['persistentSha256'] == action['beforeSha256']
                            and observations[observed_index]['persistentSha256'] == action['afterSha256'], 'Native setter state boundary')
            if name == 'first':
                entries += ['0x204bd00' if thread == 0 else '0x204bed0']
        require([item['entry'] for item in observations] == entries and len(observations) == case['actualReturningCalls'], 'Exact whole-call native order/population')
        require(observations[0]['resultWord'] == 1 and observations[2]['resultWord'] == 1, 'Native initialization/launcher results')
        require(all(item['resultWord'] == 1 for item in observations[first_start:first_start + len(case['first']['trace'])])
                and all(item['resultWord'] == 1 for item in observations[-len(case['second']['trace']):]), 'Every executed dispatch returned1')
        calls += len(observations)
    expected_coverage = {str(pc): sorted(values) for pc, values in coverage.items()}
    require(all(values == {False, True} for values in coverage.values()) and proof['ownBranchCoverage'] == expected_coverage
            and proof['allOwnBranchOutcomesCovered'] is True, 'Measured full caller branch coverage')
    require(calls == proof['actualReturningCalls'] == report['actualReturningCallsPerImplementation'] == 5378
            and report['actualReturningCallsTotal'] == 10756 and proof['freshMachines'] == report['freshMachinesPerImplementation'] == 60,
            'Actual complete caller returns/machines; bound failure excluded')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(sys.version_info[:3] == (3, 13, 5), 'Pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(node.value) for node in ast.parse(path.read_text()).body
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in node.targets))
    for name, sha in pins.items():
        checked(root, {'path': name, 'sha256': sha})
    sys.path.insert(0, str(root))
    matcher = shared.helpers.load_module(path, '_entry129_frozen_matcher')
    require(matcher.ROOT == matcher.assets.ROOT == matcher.fixtures.native.ROOT == root, 'Repository-local dependencies')
    matcher.assets.original_files.cache_clear()
    for name, sha in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
                      ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH),
                      ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': sha})
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH
            and report['sourceClosure'] == [{'path': name, 'sha256': sha} for name, sha in pins.items()], 'Frozen source/proof closure')
    data = matcher.assets.load(root / 'extract/files/s07e01.e')
    rom, files = matcher.assets.original_files()
    interval = files['s07e01.e']
    require(report['romSha256'] == matcher.assets.ROM_HASH and report['romFileRange'] == list(interval), 'Original ROM identity/layout')
    raw = (root / data['asset']).read_bytes()
    require(raw == rom[interval[0]:interval[1]] and report['archiveSha256'] == data['assetSha256']
            and report['scriptSha256'] == data['scriptSha256'] and report['codeSha256'] == digest(data['code']), 'ROM-backed original image')
    members = []
    for index in range(matcher.assets.u32(raw, 4)):
        offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
        stored = raw[offset:offset + length]
        require(matcher.assets.ash(stored) == data['script'], 'Original member alias bytes')
        members.append({'index': index, 'offset': offset, 'bytes': length, 'storedSha256': digest(stored), 'scriptSha256': data['scriptSha256']})
    require(report['members'] == members, 'No omitted archive aliases')
    allocation = json.loads((root / 'src/scripts/20261029/batch07/entry.locals.json').read_text())
    links = json.loads((root / 'src/scripts/20261029/batch07/entry.links.json').read_text())
    require(report['boundariesAndLocalStorage'] == json.loads(json.dumps(matcher.boundary(data, allocation))), 'Complete760 bounds and scratch scope')
    require(report['qualifiedOriginalScriptCallees'] == matcher.bindings(data, links), 'Qualified original zero-credit script callees')
    require(all(link['calleeSourceCredit'] == 0 and link['sourceLinkedCalleeClaimed'] is False and link['qualifiedOriginalCallee'] is True
                for link in report['qualifiedOriginalScriptCallees']), 'Original dependencies are not source-linked credit')
    require(report['namedNativeApiBindings'] == matcher.named_apis(), 'Native API dispatch identities')
    build = report['buildCommand']
    require(build['exitCode'] == 0 and build['originalBytecodeCompilerInput'] is False, 'Source-only build')
    inputs = {Path(item['path']).name: checked(root, item) for item in build['inputs']}
    expected = {'scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py', 'scr_c_compiler_20261029_v5.py',
                'process_context_entry.c', 'scr_typed_calls.h', 'entry.locals.json', 'entry.links.json'}
    require(set(inputs) == expected and len(build['inputs']) == 7, 'Exact source-only closure')
    for name, item in inputs.items():
        original = name if name.endswith('.py') else 'src/scripts/20261029/batch07/' + name
        require(digest(item.read_bytes()) == pins[original], 'Copied compiler/source/link input')
    body = checked(root, build['emittedBody']).read_bytes()
    source_report = json.loads(checked(root, build['compilerReport']).read_text())
    require(body == data['code'][BASE:END] and len(body) == 760 and source_report == report['sourceOnlyBuild'], 'Current exact emitted caller/compiler report')
    require(report['matchedRange'] == {'startPc': BASE, 'endExclusivePc': END, 'bytes': 760, 'sha256': digest(body)}, 'Full760 source gate')
    stage = root / 'work/script-source/20261029/batch07/entry129-validator'
    stage.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=stage) as temporary:
        directory = Path(temporary)
        for name, item in inputs.items():
            shutil.copyfile(item, directory / name)
        command = [sys.executable, 'scr_c_compiler_20261029_v5.py', '--source', 'process_context_entry.c', '--base', hex(BASE),
                   '--locals', 'entry.locals.json', '--links', 'entry.links.json', '--output', 'fresh.scrfunc', '--report', 'fresh.json']
        subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        require((directory / 'fresh.scrfunc').read_bytes() == body, 'Fresh source-only v5 replay')
        require(json.loads((directory / 'fresh.json').read_text()) == source_report, 'Entire v5 source/link/compiler evidence')
    require(checked(root, build['rebuiltImage']).read_bytes() == data['script'], 'Current rebuilt decoded image')
    controls = report['compilerControls']
    require(len(controls['rejectedSourceProfilesLinks']) == 15 and controls['controlSourceCredit'] == 0, 'Typed source/link negative controls')
    for item in controls['rejectedSourceProfilesLinks']:
        source = checked(root, item['source'])
        try:
            matcher.compiler.compile_source(source, BASE, item['allocation'], item['links'])
        except ValueError as error:
            require(str(error) == item['error'] and item['rejectedBeforeOutput'] is True, 'Fresh typed rejection reason')
        else:
            raise ValueError('Negative typed source/link now compiles')
    require(controls['wrongAlignedTargetChangesBytes'] is True and controls['wrongAlignedTargetRejectedByImageQualification'] is True
            and controls['failedCliPreservesOutputAndReport'] is True and controls['failedCliExitCode'] != 0, 'Wrong-link/output preservation gates')
    bound_path = checked(root, report['boundedPriorUnsupportedProof'])
    require(bound_path == root / 'evidence/encounter/scr-entry129-native-bound-20261029.json'
            and report['boundedPriorUnsupportedProof']['sha256'] == pins['evidence/encounter/scr-entry129-native-bound-20261029.json'],
            'Pinned preserved exhaustion artifact')
    bound = json.loads(bound_path.read_text())
    checked(root, {'path': bound['generator'], 'sha256': bound['generatorSha256']})
    failure = bound['failure']
    require(bound['romSha256'] == matcher.assets.ROM_HASH and bound['scriptSha256'] == data['scriptSha256']
            and bound['syntheticInputs']['controlHalfword021C0ECC'] == 0x5071, 'Preserved high-field probe identity')
    require(failure['scriptPc'] == 138716 and failure['systemOpcode'] == 143
            and failure['instructionsExecutedInFailedCall'] == 20000 and failure['actualReturn'] is False
            and failure['failedCallReturnCredit'] == 0 and failure['postFaultStateUsedForProof'] is False
            and failure['nativePcAtBound'] != hex(matcher.fixtures.native.STOP), 'Bound exhaustion is not a return')
    require(bound['sourceCredit'] == 0 and bound['outerEntry129Complete'] is False and bound['resourceErrorProven'] is False
            and bound['controlFieldSemanticMeaningProven'] is False, 'No unsupported completion/resource/semantic claim')
    native_proof(report, data)
    for key in ('scaffoldingSourceCredit', 'completeImagesRecovered', 'nativeExecutableByteCredit', 'originalScriptCalleeSourceCredit', 'nativeFunctionStubs'):
        require(report[key] == 0, 'Source scope: ' + key)
    require(report['sourceDefinitionCount'] == report['completeFunctionInstances'] == 1 and report['qualifiedScriptRangeBytes'] == 760
            and report['originalScaffoldingBytes'] == len(data['script']) - 760, 'Caller-only source accounting')
    require(report['allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared'] is True
            and report['postFaultStateUsedForProof'] is False, 'Native evidence scope')
    key = digest(data['code']), BASE
    return {key: {'codeSha256': key[0], 'scriptSha256': data['scriptSha256'], 'asset': data['asset'],
        'startPc': BASE, 'endExclusivePc': END, 'bytes': 760, 'sha256': digest(body), 'entryAliases': [129],
        'mode': 'SCR', 'vmHostProcessor': 'ARM9', 'source': 'src/scripts/20261029/batch07/process_context_entry.c',
        'sourceSha256': source_report['sourceSha256'], 'sourceDefinitionCount': 1, 'substantiveDecisionLogicBytes': 760,
        'originalScriptCalleeSourceCredit': 0, 'actualReturningCallsTotal': 10756,
        'unsupportedBoundFailureReturnCredit': 0, 'wholeImageReconstructed': False}}


if __name__ == '__main__':
    units = validate()
    print(json.dumps({'validatedUnits': len(units), 'bytes': sum(unit['bytes'] for unit in units.values())}))
