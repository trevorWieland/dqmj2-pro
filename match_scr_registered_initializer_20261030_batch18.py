import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261030/batch18'
WORK = ROOT / 'work/script-source/20261030/batch18/registered-initializer'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-registered-initializer.json'
PIN_PATHS = ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261030_v15.py',
    'nonmatching/script-source/20261029/native_scr_flags_20261029.py',
    'nonmatching/script-source/20261030/native_scr_registered_initializer_20261030.py', 'evidence/encounter/script_assets_20261029.py',
    'evidence/encounter/vm_state_20261029.py', 'src/scripts/20261030/batch18/clear_registered_keys.c',
    'src/scripts/20261030/batch18/scr_registered_globals.h', 'src/scripts/20261030/batch18/globals.bindings.json')
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261030_v15.py': '248acc6d862852666789be94e73bdc5b35ffcf822d08ca7e1398e9db24783318',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_registered_initializer_20261030.py': 'd5da3befc09ac24ff1bb986623711c6407d2ee3144c152e2021a3fbd667fb39c',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch18/clear_registered_keys.c': 'a80a041d1dba20b5af22076d74a46d7e0049b6884a00f2fe23b601f3761ffa07',
 'src/scripts/20261030/batch18/scr_registered_globals.h': 'dd27c117fd18c582c31082f553b742b1552f96e3cdc46041a4d8d95f41bc1644',
 'src/scripts/20261030/batch18/globals.bindings.json': '35b6f75a7230c6dd47a9c2d0a461fd90585d8b92b13e23390ce17eded0487cd3'}
sys.path[:0] = [str(ROOT / 'evidence/encounter'), str(ROOT / 'nonmatching/script-source/20261029'),
    str(ROOT / 'nonmatching/script-source/20261030')]
import script_assets_20261029 as assets
import native_scr_registered_initializer_20261030 as fixtures
import scr_c_compiler_20261030_v15 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def boundary(data):
    own = [row for row in data['instructions'] if 552 <= row['pc'] < 1048]
    assert [slot for slot, pc in data['entries'].items() if pc == 552] == [256]
    assert not any(552 < pc < 1048 for pc in data['entries'].values())
    assert len(own) == 22 and sum(row['bytes'] for row in own) == 496 and own[-1]['pc'] == 1044 and own[-1]['opcode'] == 1026
    incoming = []
    for row in data['instructions']:
        if row['opcode'] in (1033, 1034, 1036, 1037, 1038) and 552 <= row['argumentsRaw'][1] < 1048:
            assert 552 <= row['pc'] < 1048 or row['argumentsRaw'][1] == 552
            incoming.append({'pc': row['pc'], 'opcode': row['opcode'], 'targetPc': row['argumentsRaw'][1]})
    references = []
    for row in data['instructions']:
        op, args = row['opcode'], row['argumentsRaw']
        pairs = [(args[1], args[2], 'write'), (args[3], args[4], 'read')] if op == 1045 else []
        if 1039 <= op <= 1044:
            pairs = [(args[1], args[2], 'read'), (args[3], args[4], 'read')]
        elif 1046 <= op <= 1053:
            pairs = [(args[index], args[index + 1], 'write' if index == 1 else 'read') for index in (1, 3, 5)]
        elif op == 1035:
            pairs = [(args[1], args[2], 'read')]
        for mode, raw, access in pairs:
            if mode == 0:
                slot = assets.f32(raw)
                assert slot == int(slot) and 0 <= slot < 256
                if 3 <= slot <= 22:
                    references.append({'pc': row['pc'], 'slot': int(slot), 'access': access})
    for slot in range(3, 23):
        selected = [row for row in references if row['slot'] == slot]
        assert sum(row['access'] == 'read' for row in selected) == 1 and sum(row['access'] == 'write' for row in selected) == 2
    return {'entry': 256, 'startPc': 552, 'endExclusivePc': 1048, 'bytes': 496, 'privateReturnPc': 1044,
        'entryAliases': [256], 'knownIncomingReferences': incoming, 'publicInteriorEntries': 0, 'sharedReturnTailDetected': False,
        'allOwnRecordPcs': [row['pc'] for row in own], 'moduleGlobalSlots': list(range(3, 23)), 'privateLocalSlots': [],
        'allCurrentModuleGlobalReferences': references, 'moduleGlobalsAreNotPrivateLocals': True,
        'knownFollowingPaddingRange': [1048, 1056], 'followingPaddingSourceCredit': 0,
        'opaqueNativeComputedReferenceCoverageComplete': False, 'naturalInitializerOrRegistrationCallerReachabilityProven': False}


def build(data):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(name, name) for name in PIN_PATHS[:2]] + [('src/scripts/20261030/batch18/' + name, name)
        for name in ('clear_registered_keys.c', 'scr_registered_globals.h', 'globals.bindings.json')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, 'scr_c_compiler_20261030_v15.py', '--source', 'clear_registered_keys.c', '--base', '552',
        '--bindings', 'globals.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    assert body == data['code'][552:1048] and len(body) == 496
    rebuilt = bytearray(data['script'])
    rebuilt[4100 + 552:4100 + 1048] = body
    assert rebuilt == data['script']
    target = WORK / 'world.source-registered-initializer.scr'
    target.write_bytes(rebuilt)
    return bytes(rebuilt), {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
        'inputs': [artifact(directory / name) for unused, name in files], 'emittedBody': artifact(directory / 'generated.scrfunc'),
        'compilerReport': artifact(directory / 'build.json'), 'compilerEvidence': json.loads((directory / 'build.json').read_text()),
        'rebuiltImage': artifact(target), 'originalBytecodeCompilerInput': False}


def controls(profile):
    directory = ROOT / 'nonmatching/script-source/20261030/batch18-controls'
    directory.mkdir(parents=True, exist_ok=True)
    source = (SOURCE / 'clear_registered_keys.c').read_text()
    header = (SOURCE / 'scr_registered_globals.h').read_text()
    tests = [('unbound_assignment', source.replace('registered_key_0 =', 'unbound_key ='), header, profile),
        ('inexact_constant', source.replace('registered_key_0 = -1', 'registered_key_0 = 16777217'), header, profile),
        ('unknown_constant_object', source.replace('registered_key_0 = -1', 'registered_key_0 = unbound_key'), header, profile),
        ('global_value_copy_unsupported', source.replace('registered_key_0 = -1', 'registered_key_0 = registered_key_1'), header, profile),
        ('two_definitions', source + '\nvoid second(void) { registered_key_0 = -1; }\n', header, profile),
        ('shadowed_definition', source.replace('clear_registered_keys', 'registered_key_0'), header, profile),
        ('aliased_storage', source, header, {'globals': dict(profile['globals'], registered_key_0=4)}),
        ('out_of_bank', source, header, {'globals': dict(profile['globals'], registered_key_0=256)}),
        ('duplicate_declaration', source, header.replace('#endif', 'extern float registered_key_0;\n#endif'), profile),
        ('wrong_global_type', source, header.replace('extern float registered_key_0;', 'extern int registered_key_0;'), profile)]
    output = []
    for name, text, declarations, bindings in tests:
        target = directory / name
        target.mkdir(parents=True, exist_ok=True)
        path = target / 'control.c'
        path.write_text(text)
        (target / 'scr_registered_globals.h').write_text(declarations)
        try:
            compiler.compile_source(path, 552, bindings)
        except ValueError as error:
            output.append({'name': name, 'source': artifact(path), 'header': artifact(target / 'scr_registered_globals.h'),
                'bindings': bindings, 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Unsupported global-initializer source compiled: ' + name)
    return output


def main():
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    assert set(PINS) == set(PIN_PATHS) and all(digest((ROOT / name).read_bytes()) == pin for name, pin in PINS.items())
    data = assets.load(ROOT / 'extract/files/world.e')
    scope = boundary(data)
    rebuilt, source = build(data)
    rejected = controls(json.loads((SOURCE / 'globals.bindings.json').read_text()))
    original = fixtures.run(data['script'])
    print(json.dumps({'stage': 'original initializer complete', 'returns': original['actualReturningCalls']}), flush=True)
    compiled = fixtures.run(rebuilt)
    assert original == compiled
    unused, files = assets.original_files()
    report = {'evidenceClass': 'ordinary-C-complete-module-global-float-initializer-SCR-source-match', 'generator': Path(__file__).name,
        'generatorSha256': digest(Path(__file__).read_bytes()), 'romSha256': assets.ROM_HASH, 'romFileRange': list(files['world.e']),
        'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
        'sourceClosure': [{'path': name, 'sha256': pin} for name, pin in PINS.items()], 'boundariesAndStorage': scope, 'sourceOnlyBuild': source,
        'matchedRange': {'startPc': 552, 'endExclusivePc': 1048, 'bytes': 496, 'sha256': digest(data['code'][552:1048])},
        'compilerControls': rejected, 'differential': original, 'pairedCompleteOwnEntryExecutions': original['completeOwnEntryExecutions'] * 2,
        'pairedNativeReturningCalls': original['actualReturningCalls'] * 2, 'sourceDefinitionCount': 1, 'completeFunctionInstances': 1,
        'qualifiedScriptRangeBytes': 496, 'originalScaffoldingBytes': len(data['script']) - 496, 'scaffoldingSourceCredit': 0,
        'nativeExecutableByteCredit': 0, 'completeImagesRecovered': 0, 'nativeFunctionStubs': 0, 'postFaultStateUsedForProof': False,
        'wholeRomSourceMatch': False, 'initializationOnly': True, 'branchDecisionLogicClaimed': False,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'sourceBytes': 496, 'completeEntries': report['pairedCompleteOwnEntryExecutions'], 'nativeReturns': report['pairedNativeReturningCalls']}), flush=True)


if __name__ == '__main__':
    main()
