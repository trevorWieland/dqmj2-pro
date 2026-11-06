import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261030/batch21'
WORK = ROOT / 'work/script-source/20261030/batch21/record-capacity'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-record-capacity.json'
PIN_PATHS = ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261030_v16.py', 'scr_c_compiler_20261030_v17.py',
    'nonmatching/script-source/20261029/native_scr_flags_20261029.py', 'nonmatching/script-source/20261030/native_scr_record_capacity_20261030.py',
    'evidence/encounter/script_assets_20261029.py', 'evidence/encounter/vm_state_20261029.py',
    'src/scripts/20261030/batch21/evaluate_record_capacity.c', 'src/scripts/20261030/batch21/scr_record_capacity.h',
    'src/scripts/20261030/batch21/objects.bindings.json')
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261030_v16.py': '84ff9e84b8085d8776c623ec92c9b3e7ace9e9daa90420297f54b8090fb6f5b7',
 'scr_c_compiler_20261030_v17.py': '42258e63e255eda2ddbd21d473c613109bcd9f38dfe526a29613c5e41af761a7',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_record_capacity_20261030.py': '5334092f9383c57f44eb3989326230ce7c1c745d902217de1ec01e1e925ecafd',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch21/evaluate_record_capacity.c': '40ac4a2e4ceced4eb23c5f32a0abbb84fb3304e2d0edc1576ecb94c9131f37ba',
 'src/scripts/20261030/batch21/scr_record_capacity.h': 'c6ab49869b784b87dd99afabae296e9f00c098f713afbd8542070afb90ec2b09',
 'src/scripts/20261030/batch21/objects.bindings.json': '0f1f1fff8e17f160d4326f38de18b20fe607eb12453a24e4a8bb66c396e140a8'}
sys.path[:0] = [str(ROOT / 'evidence/encounter'), str(ROOT / 'nonmatching/script-source/20261029'), str(ROOT / 'nonmatching/script-source/20261030')]
import script_assets_20261029 as assets
import native_scr_record_capacity_20261030 as fixtures
import scr_c_compiler_20261030_v17 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def boundary(data):
    own = [row for row in data['instructions'] if 0 <= row['pc'] < 544]
    assert [slot for slot, pc in data['entries'].items() if pc == 0] == [279]
    assert not any(0 < pc < 544 for pc in data['entries'].values())
    assert sum(row['bytes'] for row in own) == 544 and own[-1]['pc'] == 540 and own[-1]['opcode'] == 1026
    incoming, references = [], []
    for row in data['instructions']:
        op, args = row['opcode'], row['argumentsRaw']
        if op in (1033, 1034, 1036, 1037, 1038) and 0 <= args[1] < 544:
            assert 0 <= row['pc'] < 544 or args[1] == 0
            incoming.append({'pc': row['pc'], 'opcode': op, 'targetPc': args[1]})
        pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read')] if op == 1045 else []
        if 1039 <= op <= 1044:
            pairs = [(args[1], args[2], 'read'), (args[3], args[4], 'read')]
        elif 1046 <= op <= 1053:
            pairs = [(args[i], args[i + 1], 'write' if i == 1 else 'read') for i in (1, 3, 5)]
        elif op == 1035:
            pairs = [(args[1], args[2], 'read')]
        for mode, raw, access in pairs:
            if mode == 0:
                slot = assets.f32(raw)
                assert slot == int(slot) and 0 <= slot < 256
                if slot in (0, 1, 2):
                    references.append({'pc': row['pc'], 'slot': int(slot), 'access': access, 'insideOwnRange': row['pc'] < 544})
    return {'entry': 279, 'startPc': 0, 'endExclusivePc': 544, 'bytes': 544, 'privateReturnPc': 540, 'entryAliases': [279],
        'publicInteriorEntries': 0, 'sharedReturnTailDetected': False, 'knownIncomingReferences': incoming,
        'moduleGlobalSlots': [0, 1, 2], 'privateLocalSlots': [], 'argumentBankLiveIns': [0], 'argumentBankCallClobbers': [0],
        'allKnownModuleGlobalReferences': references, 'moduleAndArgumentObjectsAreNotPrivateLocals': True,
        'allOwnRecordPcs': [row['pc'] for row in own], 'followingPaddingRange': [544, 552], 'followingPaddingSourceCredit': 0,
        'opaqueNativeComputedReferenceCoverageComplete': False, 'naturalCallerReachabilityProven': False}


def build(data):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(ROOT / name, name) for name in PIN_PATHS[:3]] + [(SOURCE / name, name) for name in
        ('evaluate_record_capacity.c', 'scr_record_capacity.h', 'objects.bindings.json')]
    for path, name in files:
        shutil.copyfile(path, directory / name)
    command = [sys.executable, 'scr_c_compiler_20261030_v17.py', '--source', 'evaluate_record_capacity.c', '--base', '0',
        '--bindings', 'objects.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    assert body == data['code'][:544] and len(body) == 544
    rebuilt = bytearray(data['script'])
    rebuilt[4100:4100 + 544] = body
    assert rebuilt == data['script']
    target = WORK / 'world.source-record-capacity.scr'
    target.write_bytes(rebuilt)
    return bytes(rebuilt), {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
        'inputs': [artifact(directory / name) for unused, name in files], 'emittedBody': artifact(directory / 'generated.scrfunc'),
        'compilerReport': artifact(directory / 'build.json'), 'compilerEvidence': json.loads((directory / 'build.json').read_text()),
        'rebuiltImage': artifact(target), 'originalBytecodeCompilerInput': False}


def controls():
    text = (SOURCE / 'evaluate_record_capacity.c').read_text()
    header = (SOURCE / 'scr_record_capacity.h').read_text()
    profile = json.loads((SOURCE / 'objects.bindings.json').read_text())
    alias, argument, outside = [json.loads(json.dumps(profile)) for unused in range(3)]
    alias['objects']['capacity_result'] = {'bank': 0, 'slot': 1}
    argument['objects']['capacity_result'] = {'bank': 1, 'slot': 1}
    outside['objects']['capacity_result'] = {'bank': 0, 'slot': 256}
    tests = [('alias', text, header, alias), ('argument_destination', text, header, argument), ('slot256', text, header, outside),
        ('no_final_return', text.replace('return capacity_result;', ''), header, profile),
        ('extra_return', text.replace('capacity_result = 1;', 'return capacity_result;', 1), header, profile),
        ('unknown_object', text.replace('capacity_result = 0;', 'capacity_result = unknown;'), header, profile),
        ('undeclared_parent_constant', text.replace('capacity_result = 0;', 'capacity_result = object_category;'), header, profile),
        ('wrong_getter_type', text, header.replace('float get_unoccupied_native_record_count', 'int get_unoccupied_native_record_count'), profile),
        ('getter_argument', text.replace('get_unoccupied_native_record_count()', 'get_unoccupied_native_record_count(1)'), header, profile),
        ('unsupported_comparison', text.replace('1 <= sampled_unoccupied_count', '1 > sampled_unoccupied_count'), header, profile)]
    output = []
    for name, source, declarations, bindings in tests:
        directory = ROOT / 'nonmatching/script-source/20261030/batch21-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / 'control.c'
        path.write_text(source)
        (directory / 'scr_record_capacity.h').write_text(declarations)
        try:
            compiler.compile_source(path, 0, bindings)
        except ValueError as error:
            output.append({'name': name, 'source': artifact(path), 'header': artifact(directory / 'scr_record_capacity.h'),
                'bindings': bindings, 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Unsupported capacity source compiled: ' + name)
    return output


def main():
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    assert set(PINS) == set(PIN_PATHS) and all(digest((ROOT / name).read_bytes()) == pin for name, pin in PINS.items())
    assert fixtures.native.ROOT == ROOT and all(digest(blob) == pin for blob, pin in
        ((fixtures.native.MAIN, fixtures.native.MAIN_HASH), (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH), (fixtures.native.ITCM, fixtures.native.ITCM_HASH)))
    data = assets.load(ROOT / 'extract/files/world.e')
    scope = boundary(data)
    rebuilt, source = build(data)
    rejected = controls()
    original = fixtures.run(data['script'])
    print(json.dumps({'stage': 'original capacity complete', 'returns': original['actualReturningCalls']}), flush=True)
    compiled = fixtures.run(rebuilt)
    assert original == compiled
    parts = [part for case in original['cases'] for part in (case['first'], case['second'])]
    unused, files = assets.original_files()
    report = {'evidenceClass': 'ordinary-C-complete-native-record-capacity-decision-SCR-source-match', 'generator': Path(__file__).name,
        'generatorSha256': digest(Path(__file__).read_bytes()), 'romSha256': assets.ROM_HASH, 'romFileRange': list(files['world.e']),
        'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
        'nativeSourceRoot': str(fixtures.native.ROOT), 'sourceClosure': [{'path': name, 'sha256': pin} for name, pin in PINS.items()],
        'boundariesAndStorage': scope, 'sourceOnlyBuild': source, 'compilerControls': rejected, 'differential': original,
        'matchedRange': {'startPc': 0, 'endExclusivePc': 544, 'bytes': 544, 'sha256': digest(data['code'][:544])},
        'pairedCompleteOwnEntryExecutions': original['completeOwnEntryExecutions'] * 2, 'pairedNativeReturningCalls': original['actualReturningCalls'] * 2,
        'pairedActualNestedCounterReturns': sum(len(part['nativeCounterReturns']) for part in parts) * 2,
        'sourceDefinitionCount': 1, 'completeFunctionInstances': 1, 'qualifiedScriptRangeBytes': 544, 'originalScaffoldingBytes': len(data['script']) - 544,
        'scaffoldingSourceCredit': 0, 'nativeExecutableByteCredit': 0, 'completeImagesRecovered': 0, 'nativeFunctionStubs': 0,
        'postFaultStateUsedForProof': False, 'wholeRomSourceMatch': False, 'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True,
        'nativeCounterIdentity': {'syscall': 187, 'handler': 'main:ARM02052DBC', 'counter': 'main:ARM020629E0',
        'secondaryCounters': ['main:ARM02062AA0', 'main:ARM02062AD0'], 'recordBase': '0x21bd674', 'recordStride': 132, 'recordCount': 100, 'testedNonzeroWordOffset': 20},
        'nativeRecordValidityOwnershipImportLegalityOrNaturalSceneReachabilityProven': False}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'sourceBytes': 544, 'completeEntries': report['pairedCompleteOwnEntryExecutions'], 'nativeReturns': report['pairedNativeReturningCalls']}), flush=True)


if __name__ == '__main__':
    main()
