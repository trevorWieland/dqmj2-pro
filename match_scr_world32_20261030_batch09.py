import hashlib
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261030/batch09'
WORK = ROOT / 'work/script-source/20261030/batch09/world32'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-world32.json'
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261029_v4.py': '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7',
 'scr_c_compiler_20261030_v6.py': 'ea44995cc5d9e13810a3d8f896b830a75b2cd42665a56b26d8289ef39df781a5',
 'scr_c_compiler_20261030_v7.py': '20b9bfed558c5d4bbd2962e4f58841db473e44723c2653498139c31621edbf26',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_world32_20261030.py': 'f219a4d3d54cecf482d2eaf47949033b4746b1f3b73a1afd6bd5cd92f2201b5e',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch09/reset_world_flags.c': '8c39b5b0726c72eb28e1f19c6630b5fb9edb35d83a38f089aa846fdc9e613ded',
 'src/scripts/20261030/batch09/scr_reset_caller.h': 'cff18e5316e7f739e4f2bb5c4ee6f5e9130f39821c17709c922e02f2d0a354be',
 'src/scripts/20261030/batch09/reset.locals.json': 'd9134abf671bd2338ce17a02515a9b8bd45d89b02229ba5f118563158d281f5c',
 'src/scripts/20261030/batch09/reset.links.json': 'e585d88e8196043841ece245e500dede5537f4d6aa42cf699a1b7f3b2a022acb',
 'src/scripts/20261030/batch08/advance_world_state.c': 'a37916359e3cd70b6df1813b7dc1e597f910d6e90691ccca38f81f31d3476259',
 'src/scripts/20261030/batch08/scr_world_state.h': '1925a586fd944285694802df3d149355be853f4a81cadb17828550bf11658b2b',
 'src/scripts/20261030/batch08/world.bindings.json': 'ed204331ed62ff1d1ac7a927758f7108607701704463f277cd3e448d576169a5',
 'src/scripts/20261029/batch02/before_primary_flag_reset.c': 'c6e2d8d816a96553043687a44c00d98f3c9c3c7d98db68a290c4e8a590e86d6d',
 'src/scripts/20261029/batch02/scr_flags.h': '8f0e2b3942eb2760b8fff0031849b4738c5e16c96cfd27e2e4a269bbddc9f7fe'}
for path, sha in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261030'))
import script_assets_20261029 as assets
import native_scr_world32_20261030 as fixtures
import scr_c_compiler_20261030_v7 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def native_contracts():
    result, image = {}, fixtures.native.MAIN
    for name, opcode in (('sample_signed_random', 36), ('reset_runtime_counter', 43),
                         ('runtime_counter_at_threshold', 48), ('set_numeric_state', 40), ('set_primary_flag', 42)):
        address = 0x0205A68C + opcode * 4
        delta = struct.unpack_from('<I', image, address - 0x02000000)[0] & 0xFFFFFF
        delta -= 0x1000000 if delta & 0x800000 else 0
        case = address + 8 + delta * 4
        calls = []
        for pc in range(case, case + 40, 4):
            word = struct.unpack_from('<I', image, pc - 0x02000000)[0]
            if word >> 24 == 0xEA:
                break
            if word >> 24 == 0xEB:
                displacement = word & 0xFFFFFF
                displacement -= 0x1000000 if displacement & 0x800000 else 0
                calls.append(pc + 8 + displacement * 4)
        assert len(calls) == 1
        result[name] = {'systemOpcode': opcode, 'nativeCasePc': case, 'nativeWrapper': calls[0],
            'processor': 'ARM9', 'module': 'main', 'mode': 'ARM', 'moduleSha256': fixtures.native.MAIN_HASH, 'sourceCredit': 0}
    return result


def boundary(data, profile, links):
    base, end = fixtures.BASE, fixtures.END
    assert [slot for slot, pc in data['entries'].items() if pc == base] == [32]
    assert not any(base < pc < end for pc in data['entries'].values())
    own = [row for row in data['instructions'] if base <= row['pc'] < end]
    assert sum(row['bytes'] for row in own) == 3740 and own[-1]['pc'] == end - 4 and own[-1]['opcode'] == 1026
    assert sum(row['opcode'] == 1026 for row in own) == 1
    references, incoming = {name: [] for name in profile}, []
    by_slot = {slot: name for name, slot in profile.items()}
    for row in data['instructions']:
        op, args = row['opcode'], row['argumentsRaw']
        if op in (1033, 1034, 1036, 1037, 1038) and base <= args[1] < end:
            incoming.append({'sourcePc': row['pc'], 'targetPc': args[1], 'opcode': op})
            assert not (base < args[1] < end and not base <= row['pc'] < end)
        pairs = []
        if op == 1045:
            pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read')]
        elif 1039 <= op <= 1044:
            pairs = [(args[1], args[2], 'read'), (args[3], args[4], 'read')]
        elif 1046 <= op <= 1053:
            pairs = [(args[i], args[i + 1], 'write' if i == 1 else 'read') for i in (1, 3, 5)]
        elif op == 1035:
            pairs = [(args[1], args[2], 'read')]
        for mode, raw, access in pairs:
            if mode != 0:
                continue
            slot = struct.unpack('<f', struct.pack('<I', raw))[0]
            assert slot == int(slot) and 0 <= slot < 256
            if int(slot) in by_slot:
                assert base <= row['pc'] < end
                references[by_slot[int(slot)]].append({'pc': row['pc'], 'access': access})
    for name, item in links.items():
        start, finish = item['entryPc'], item['endExclusivePc']
        assert start in data['entries'].values()
        assert item['scriptSha256'] == data['scriptSha256'] and item['codeSha256'] == digest(data['code'])
        assert item['rangeSha256'] == digest(data['code'][start:finish])
        assert item['dependencyKind'] == ('source-linked' if start in (64268, 59052) else 'qualified-original')
    return {'entry': 32, 'startPc': base, 'endExclusivePc': end, 'bytes': 3740, 'privateReturnPc': end - 4,
        'knownIncomingReferences': incoming, 'knownSlotReferences': references, 'knownOutsideSlotReferences': 0,
        'allKnownMode0IndicesCanonical': True, 'opaqueNativeOrComputedSlotReferenceCoverageComplete': False,
        'externalInteriorEntries': 0, 'sharedReturnTailDetected': False, 'serializedCompleteCallsOnly': True,
        'originalCalleeSourceCredit': 0, 'sourceLinkedCalleesNewCredit': 0}


def compile_unit(name, files, command):
    directory = WORK / name
    directory.mkdir(parents=True, exist_ok=True)
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    argv = [sys.executable, *command, '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(argv, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    return (directory / 'generated.scrfunc').read_bytes(), {'command': argv, 'cwd': str(directory),
        'exitCode': result.returncode, 'stdout': result.stdout.strip(), 'inputs': [artifact(directory / target) for unused, target in files],
        'emittedBody': artifact(directory / 'generated.scrfunc'), 'compilerReport': artifact(directory / 'build.json'),
        'compilerEvidence': json.loads((directory / 'build.json').read_text()), 'originalBytecodeCompilerInput': False}


def build(data):
    common = [(name, name) for name in ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py')]
    units = [('caller', 60232, 63972, common + [('scr_c_compiler_20261030_v7.py', 'scr_c_compiler_20261030_v7.py')] +
        [('src/scripts/20261030/batch09/' + name, name) for name in ('reset_world_flags.c', 'scr_reset_caller.h', 'reset.locals.json', 'reset.links.json')],
        ['scr_c_compiler_20261030_v7.py', '--source', 'reset_world_flags.c', '--base', hex(60232), '--locals', 'reset.locals.json', '--links', 'reset.links.json']),
        ('linked-entry34', 64268, 65620, common + [('scr_c_compiler_20261030_v6.py', 'scr_c_compiler_20261030_v6.py')] +
        [('src/scripts/20261030/batch08/' + name, name) for name in ('advance_world_state.c', 'scr_world_state.h', 'world.bindings.json')],
        ['scr_c_compiler_20261030_v6.py', '--source', 'advance_world_state.c', '--base', hex(64268), '--bindings', 'world.bindings.json']),
        ('linked-entry20', 59052, 59068, [('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029.py')] +
        [('src/scripts/20261029/batch02/' + name, name) for name in ('before_primary_flag_reset.c', 'scr_flags.h')],
        ['scr_c_compiler_20261029.py', '--source', 'before_primary_flag_reset.c', '--base', hex(59052)])]
    rebuilt, reports = bytearray(data['script']), []
    for name, start, end, inputs, command in units:
        body, report = compile_unit(name, inputs, command)
        assert body == data['code'][start:end] and len(body) == end - start
        rebuilt[4100 + start:4100 + end] = body
        reports.append({'kind': 'new-caller' if name == 'caller' else 'existing-source-linked-callee-reuse',
            'startPc': start, 'endExclusivePc': end, 'bytes': len(body), 'sourceCredit': len(body) if name == 'caller' else 0,
            'build': report})
    assert bytes(rebuilt) == data['script']
    output = WORK / 'world.source-linked.scr'
    output.write_bytes(rebuilt)
    return bytes(rebuilt), reports, artifact(output)


def controls(profile, links):
    directory = ROOT / 'nonmatching/script-source/20261030/batch09-controls'
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_reset_caller.h', directory / 'scr_reset_caller.h')
    text = (SOURCE / 'reset_world_flags.c').read_text()
    bad_alias = dict(profile, runtime_limit=101)
    wrong_arity = json.loads(json.dumps(links))
    wrong_arity['apply_saved_world_argument']['argumentTypes'] = []
    tests = [('alias', text, bad_alias, links), ('missing_formal', text, {k: v for k, v in profile.items() if k != 'saved_input'}, links),
        ('unbounded_flag_value', text.replace('set_primary_flag(145, runtime_limit)', 'set_primary_flag(145, saved_input)'), profile, links),
        ('unbounded_numeric_value', text.replace('set_numeric_state(52, sampled_value)', 'set_numeric_state(52, saved_input)'), profile, links),
        ('rng_zero', text.replace('sample_signed_random(7)', 'sample_signed_random(0)'), profile, links),
        ('rng_overflow', text.replace('sample_signed_random(7)', 'sample_signed_random(257)'), profile, links),
        ('counter_nonzero', text.replace('reset_runtime_counter(0)', 'reset_runtime_counter(1)'), profile, links),
        ('bad_getter_type', text.replace('bool runtime_limit', 'float runtime_limit'), profile, links),
        ('missing_link', text, profile, {k: v for k, v in links.items() if k != 'finalize_world_state'}),
        ('link_abi', text, profile, wrong_arity),
        ('call_arity', text.replace('finalize_world_state()', 'finalize_world_state(saved_input)'), profile, links),
        ('negative_flag', text.replace('set_primary_flag(2, false)', 'set_primary_flag(-1, false)'), profile, links),
        ('runtime_loop', text.replace('flag < 510', 'flag < saved_input'), profile, links)]
    rejected = []
    for name, source, allocation, bindings in tests:
        path = directory / (name + '.c')
        path.write_text(source)
        try:
            compiler.compile_source(path, fixtures.BASE, allocation, bindings)
        except (ValueError, TypeError) as error:
            rejected.append({'name': name, 'source': artifact(path), 'profile': allocation, 'links': bindings,
                             'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Negative reset-caller control accepted: ' + name)
    wrong = json.loads(json.dumps(links))
    wrong['reset_shared_flags']['entryPc'] += 4
    body, unused = compiler.compile_source(SOURCE / 'reset_world_flags.c', fixtures.BASE, profile, wrong)
    return {'rejectedSourceProfilesLinks': rejected, 'wrongAlignedBindingChangesBytes': body != (WORK / 'caller/generated.scrfunc').read_bytes(),
            'wrongAlignedBindingQualifiedAgainstCurrentImage': False, 'negativeControlSourceCredit': 0}


def main():
    assert unicorn.__version__ == '2.1.4'
    for image, sha in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH), (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH),
                       (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == sha
    WORK.mkdir(parents=True, exist_ok=True)
    data = assets.load(ROOT / 'extract/files/world.e')
    assert data['scriptSha256'] == '9c6c4a136b306126a83a8a749df18276aa2a9d328a4add073fc47f50ea0619f8'
    profile = json.loads((SOURCE / 'reset.locals.json').read_text())
    links = json.loads((SOURCE / 'reset.links.json').read_text())
    bounds = boundary(data, profile, links)
    rebuilt, builds, product = build(data)
    negative = controls(profile, links)
    original = fixtures.run(data['script'])
    recompiled = fixtures.run(rebuilt)
    assert original == recompiled
    owned = {row['pc'] for row in data['instructions'] if fixtures.BASE <= row['pc'] < fixtures.END}
    executed = {row['pc'] for case in original['cases'] for key in ('first', 'second') for row in case[key]['trace'] if row['pc'] in owned}
    assert owned == executed
    rom, files = assets.original_files()
    report = {'schemaVersion': 1, 'generator': Path(__file__).relative_to(ROOT).as_posix(), 'generatorSha256': digest(Path(__file__).read_bytes()),
        'evidenceClass': 'ordinary-C-complete-reset-caller-with-source-linked-SCR-callees',
        'reproductionCommand': 'python match_scr_world32_20261030_batch09.py',
        'sourceClosure': [{'path': path, 'sha256': sha} for path, sha in PINS.items()], 'romSha256': assets.ROM_HASH,
        'asset': data['asset'], 'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
        'romFileRange': list(files['world.e']), 'matchedRange': {'startPc': fixtures.BASE, 'endExclusivePc': fixtures.END, 'bytes': 3740,
        'sha256': builds[0]['build']['compilerEvidence']['outputSha256']}, 'boundariesAndLinks': bounds,
        'sourceOnlyBuilds': builds, 'rebuiltDecodedImage': product, 'compilerControls': negative, 'differential': original,
        'namedNativeApiContracts': native_contracts(),
        'executedOwnRecordPcs': sorted(executed), 'allOwnRecordsExecuted': True,
        'sourceDefinitionCount': 1, 'completeFunctionInstances': 1, 'qualifiedScriptRangeBytes': 3740,
        'reusedSourceLinkedCalleeBytes': 1368, 'reusedSourceLinkedCalleeNewCredit': 0, 'qualifiedOriginalCalleeCount': 5,
        'qualifiedOriginalCalleeSourceCredit': 0, 'scaffoldingSourceCredit': 0, 'completeImagesRecovered': 0, 'nativeExecutableByteCredit': 0,
        'actualReturningCallsPerImplementation': original['actualReturningCalls'], 'actualReturningCallsTotal': original['actualReturningCalls'] * 2,
        'freshMachinesPerImplementation': original['freshMachines'], 'nativeFunctionStubs': 0, 'postFaultStateUsedForProof': False,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True, 'wholeRomSourceMatch': False,
        'limitations': ['Complete3740B caller only; five qualified original script callees remain zero-credit source dependencies',
            'Entry34 and empty20 are freshly source-compiled and included in the executed linked image with zero duplicate credit',
            'Native counter/RNG/threshold facts carry no timing, story, access or encounter-renewal meanings',
            'Supported synthetic numeric0/1 context is4/0; all4threads and signedzero/one/quietNaN formal words are tested',
            'Known encoded slot references are audited; opaque/native/computed access coverage remains incomplete']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(OUTPUT), 'bytes': 3740, 'actualReturns': report['actualReturningCallsTotal'],
                      'freshMachinesPerImplementation': original['freshMachines'], 'negativeControls': len(negative['rejectedSourceProfilesLinks'])}))


if __name__ == '__main__':
    main()
