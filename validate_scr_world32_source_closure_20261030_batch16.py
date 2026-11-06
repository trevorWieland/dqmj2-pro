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
OLD = ROOT / 'validate_scr_world32_20261030_batch09.py'
assert hashlib.sha256(OLD.read_bytes()).hexdigest() == '7201eb2f9e39a344cd3ecb3929bf4403bc7a1445553b834bd8481f1c068b33d1'
SPEC = importlib.util.spec_from_file_location('_world32_closure_frozen_validator', OLD)
legacy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(legacy)
require, checked, digest, local = legacy.require, legacy.checked, legacy.digest, legacy.local
MATCHER = 'match_scr_world32_source_closure_20261030_batch16.py'
MATCHER_HASH = '37244678ce8f983eff3a2dc84d8db8584c38515097d6647e368cc844a32c9074'
REPORT = 'evidence/matches/scripts-20261030-world32-source-closure.json'


def native_proof(report, data):
    proof = report['differential']
    require(proof['freshMachines'] == len(proof['cases']) == 16 and proof['all4Threads'] is True
        and proof['nativeInstructionCap'] == 20000 and proof['nativeTimeoutMicroseconds'] == 1000000 and proof['scriptStepBound'] == 3000
        and proof['serializedCompleteCallsOnly'] is True and proof['naturalSceneOrRenewabilityMeaningProven'] is False,
        'Bounded serialized root execution scope')
    words, counters, rngs = [0, 0x80000000, 0x3F800000, 0x7FC00001], [0, 10799, 10800, 0xFFFFFFFF], [0, 1, 0xFFFFFFFF, 0x12345678]
    decoded, calls, callee_executions = {row['pc']: row for row in data['instructions']}, 0, 0
    for index, case in enumerate(proof['cases']):
        phase, thread = divmod(index, 4)
        seed, input_word, rng = 2026103009500 + index, words[phase], rngs[(phase + thread) % 4]
        pattern, gate = bool(thread & 1), bool((phase + thread) & 1)
        require((case['thread'], case['seed'], case['inputWord'], case['thresholdCounter'], case['rngSeed'], case['initialClearFlags'], case['numeric20Gate']) ==
            (thread, seed, input_word, counters[phase], rng, pattern, gate), 'Qualified root scenario identity')
        state = bytearray(random.Random(seed).randbytes(0x7040))
        state[legacy.NUMERIC - legacy.PERSIST:legacy.NUMERIC + 2 - legacy.PERSIST] = bytes((4, 0))
        state[legacy.NUMERIC + 20 - legacy.PERSIST], state[legacy.NUMERIC + 28 - legacy.PERSIST] = 28 if gate else 27, 5
        legacy.set_bit(state, 218, True)
        for flag in legacy.CLEAR_FLAGS:
            legacy.set_bit(state, flag, pattern)
        struct.pack_into('<I', state, 4, counters[phase])
        registers = random.Random(seed ^ 0x947).randbytes(1024)
        observed = case['observations']
        legacy.shared.observations(observed)
        startup = ['0x204bc08', '0x204bd00'] + ['0x204bed0'] * thread
        require([row['entry'] for row in observed[:len(startup)]] == startup, 'Natural root start/forks')
        cursor = len(startup)
        for ordinal, name in enumerate(('first', 'second')):
            if ordinal:
                require(observed[cursor]['entry'] == ('0x204bd00' if thread == 0 else '0x204bed0'), 'Natural serialized root reentry')
                cursor += 1
                rng = case['first']['rngAfter']
            part = case[name]
            finish = cursor + len(part['trace'])
            state, registers = legacy.invocation(part, bytes(state), registers, input_word, rng, decoded, observed[cursor:finish])
            require(len(part['directScriptCalls']) == 7, 'All seven actual source-callee calls')
            callee_executions += 7
            cursor = finish
        require(cursor == len(observed) == case['actualReturningCalls'], 'Actual root native-return population')
        calls += cursor
    require(calls == proof['actualReturningCalls'] == 26038 and report['pairedNativeReturningCalls'] == calls * 2
        and report['pairedCompleteRootEntryExecutions'] == 64 and callee_executions == 224,
        'Separate actual root/native/callee counts')


def validate(root=ROOT, report_path=None):
    root = Path(root).resolve()
    require(root == ROOT and sys.version_info[:3] == (3, 13, 5), 'Local pinned Python')
    path = checked(root, {'path': MATCHER, 'sha256': MATCHER_HASH})
    pins = next(ast.literal_eval(row.value) for row in ast.parse(path.read_text()).body if isinstance(row, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'PINS' for target in row.targets))
    for name, pin in pins.items():
        checked(root, {'path': name, 'sha256': pin})
    sys.path.insert(0, str(root))
    matcher = legacy.shared.helpers.load_module(path, '_world32_source_closure_matcher')
    for name, pin in (('extract/arm9/arm9.bin', matcher.fixtures.native.MAIN_HASH),
            ('extract/arm9_overlays/ov000.bin', matcher.fixtures.native.OVERLAY_HASH), ('extract/arm9/itcm.bin', matcher.fixtures.native.ITCM_HASH)):
        checked(root, {'path': name, 'sha256': pin})
    matcher.assets.original_files.cache_clear()
    data = matcher.assets.load(root / 'extract/files/world.e')
    report = json.loads(local(root, REPORT if report_path is None else report_path).read_text())
    require(report['evidenceClass'] == 'existing-ordinary-C-eight-range-direct-SCR-source-link-closure-proof'
        and report['generator'] == MATCHER and report['generatorSha256'] == MATCHER_HASH and report['sourceClosure'] ==
        [{'path': name, 'sha256': pin} for name, pin in pins.items()], 'Frozen source-link proof identity/closure')
    require(report['romSha256'] == matcher.assets.ROM_HASH and report['scriptSha256'] == data['scriptSha256']
        and report['codeSha256'] == digest(data['code']), 'Current original ROM/script identity')
    original_links = json.loads((root / 'src/scripts/20261030/batch09/reset.links.json').read_text())
    derived = {name: {**value, 'dependencyKind': 'source-linked'} for name, value in original_links.items()}
    link = report['sourceLinking']
    require(link['originalLinkProfile'] == original_links and link['derivedSourceLinkProfile'] == derived
        and link['allSevenDirectLinksSourceLinked'] is True and link['addressesTypesHashesUnchanged'] is True
        and link['originalScrCalleeBodiesUsedForSevenLinks'] == 0 and link['knownDirectScrCallTreeOnly'] is True
        and link['opaqueNativeOrComputedGlobalClosureProven'] is False, 'Seven source-only links/exact unchanged link identities')
    products = report['products']
    require(len(products) == len(matcher.UNITS) == 8, 'Complete eight-range source closure')
    stage = root / 'work/script-source/20261030/batch16/validator'
    stage.mkdir(parents=True, exist_ok=True)
    for product, unit in zip(products, matcher.UNITS):
        name, start, end, compiler, source_root, files, arguments = unit
        require((product['name'], product['startPc'], product['endExclusivePc'], product['bytes']) == (name, start, end, end - start)
            and product['sha256'] == digest(data['code'][start:end]) and product['exitCode'] == 0
            and product['originalBytecodeCompilerInput'] is False and product['newSourceRangeCredit'] == product['newSourceDefinitionCredit'] == 0,
            'Current qualified reused source range/no excess credit')
        command = [sys.executable, compiler, *arguments, '--base', hex(start), '--output', 'generated.scrfunc', '--report', 'build.json']
        require(product['command'] == command and product['cwd'] == str(matcher.WORK / name), 'Actual source-only unit command/directory')
        inputs = {Path(row['path']).name: checked(root, row) for row in product['inputs']}
        expected = set(matcher.COMPILERS) | set(files) | ({'source-linked.links.json'} if name == 'world32' else set())
        require(set(inputs) == expected and len(inputs) == len(product['inputs']), 'Exact source-only compilation input set')
        for filename, candidate in inputs.items():
            if filename == 'source-linked.links.json':
                require(json.loads(candidate.read_text()) == derived, 'Generated source-linked profile is exact kind-only transformation')
            else:
                origin = filename if filename in matcher.COMPILERS else source_root + '/' + filename
                require(digest(candidate.read_bytes()) == pins[origin], 'Copied frozen source/compiler/profile input')
        body = checked(root, product['emittedBody']).read_bytes()
        compiled = json.loads(checked(root, product['compilerReport']).read_text())
        require(body == data['code'][start:end] and compiled == product['compilerEvidence'], 'Actual source product/current whole range')
        if name == 'world32':
            require(compiled['qualifiedLinks'] == derived and checked(root, product['derivedLinkProfile']) == inputs['source-linked.links.json'],
                'Caller compiled with all actual source-linked dependencies')
        with tempfile.TemporaryDirectory(prefix=name + '-', dir=stage) as temporary:
            directory = Path(temporary)
            for filename, candidate in inputs.items():
                shutil.copyfile(candidate, directory / filename)
            subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
            fresh = json.loads((directory / 'build.json').read_text())
            require((directory / 'generated.scrfunc').read_bytes() == body, 'Fresh isolated exact source product for every linked range')
            if name == 'world20':
                paths = {'sourcePath': 'before_primary_flag_reset.c', 'includePath': 'scr_flags.h', 'compilerPath': compiler}
                require(all(fresh[key] == str((directory / filename).resolve()) and compiled[key] == str((matcher.WORK / name / filename).resolve())
                    for key, filename in paths.items()), 'Measured v1 source/include/compiler execution paths')
                require({key: value for key, value in fresh.items() if key not in paths} ==
                    {key: value for key, value in compiled.items() if key not in paths}, 'All path-independent v1 source/compiler evidence')
            else:
                require(fresh == compiled, 'Fresh isolated source-only compiler evidence for every linked range')
    require(link['physicalReusedSourceRangeBytes'] == sum(row['bytes'] for row in products) == 10308 and link['callerBytes'] == 3740
        and link['calleeProductBytes'] == 6568 and checked(root, link['rebuiltImage']).read_bytes() == data['script'], 'Exact rebuilt eight-range image')
    native_proof(report, data)
    require(all(report[name] == 0 for name in ('newSourceRangeCredit', 'newSourceByteCredit', 'newSourceDefinitionCredit', 'nativeSourceCredit', 'completeImageCredit'))
        and report['wholeRomSourceMatch'] is False, 'Zero duplicate/native/full-image credit')
    return {'validatedSourceLinkedRanges': 8, 'actualSourceLinkedDirectCallees': 7, 'reusedSourceBytes': 10308,
        'pairedCompleteRootEntryExecutions': 64, 'pairedCompleteDirectCalleeExecutions': 448, 'pairedNativeReturningCalls': 52076,
        'newSourceCredit': 0, 'completeImageCredit': 0, 'nativeSourceCredit': 0}


if __name__ == '__main__':
    print(json.dumps(validate()))
