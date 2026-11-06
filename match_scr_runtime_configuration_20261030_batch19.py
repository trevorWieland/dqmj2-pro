import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/script-source/20261030/batch19/runtime-configuration'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-runtime-configuration.json'
PIN_PATHS = ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261030_v16.py',
    'nonmatching/script-source/20261029/native_scr_flags_20261029.py', 'nonmatching/script-source/20261030/native_scr_runtime_configuration_20261030.py',
    'evidence/encounter/script_assets_20261029.py', 'evidence/encounter/vm_state_20261029.py',
    'src/scripts/20261030/batch19/object6/configure_primary_object6.c', 'src/scripts/20261030/batch19/object6/scr_runtime_configuration.h',
    'src/scripts/20261030/batch19/object6/objects.bindings.json', 'src/scripts/20261030/batch19/object7/configure_primary_object7.c',
    'src/scripts/20261030/batch19/object7/scr_runtime_configuration.h', 'src/scripts/20261030/batch19/object7/objects.bindings.json')
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261030_v16.py': '84ff9e84b8085d8776c623ec92c9b3e7ace9e9daa90420297f54b8090fb6f5b7',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_runtime_configuration_20261030.py': '3a2300dcf4351d22b6b45ebaa23cbbe175ae70f5fe61b63ae249e307465810ee',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch19/object6/configure_primary_object6.c': '7a1482b52612069fdb081cb7ebeaf707a082083cc91eb90324a567cc6a987ecb',
 'src/scripts/20261030/batch19/object6/scr_runtime_configuration.h': '6fb54eb50dc6deb3c44ac39e73b61fa3d3411783e7b9ae3c36bb963a76768f79',
 'src/scripts/20261030/batch19/object6/objects.bindings.json': '92e28dc477067eeda866b2ceab66e13a391da8e63362f75b7315ba46e5aa7d81',
 'src/scripts/20261030/batch19/object7/configure_primary_object7.c': '66aa8f9e3077cda741e11107c27100b8da048a43f9ef54391caa4838b0145f63',
 'src/scripts/20261030/batch19/object7/scr_runtime_configuration.h': '25c67cc611e55846c156553275af7dc251db57b7790f3d07b4f5950f4caab804',
 'src/scripts/20261030/batch19/object7/objects.bindings.json': '5e4be97b1b42b13fb76f1ecede653ee117b0aad9ca7ba73d5382b0c67f1891a0'}
sys.path[:0] = [str(ROOT / 'evidence/encounter'), str(ROOT / 'nonmatching/script-source/20261029'), str(ROOT / 'nonmatching/script-source/20261030')]
import script_assets_20261029 as assets
import native_scr_runtime_configuration_20261030 as fixtures
import scr_c_compiler_20261030_v16 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def boundary(data, unit):
    entry, start, end, category, selected = unit
    own = [row for row in data['instructions'] if start <= row['pc'] < end]
    require = lambda condition: condition or (_ for _ in ()).throw(ValueError('Configuration direct/complete boundary failure'))
    require([slot for slot, pc in data['entries'].items() if pc == start] == [entry])
    require(not any(start < pc < end for pc in data['entries'].values()))
    require(sum(row['bytes'] for row in own) == 624 and own[-1]['opcode'] == 1026 and own[-1]['pc'] == end - 4)
    incoming, references = [], []
    for row in data['instructions']:
        op, args = row['opcode'], row['argumentsRaw']
        if op in (1033, 1034, 1036, 1037, 1038) and start <= args[1] < end:
            require(start <= row['pc'] < end or args[1] == start)
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
                require(slot == int(slot) and 0 <= slot < 256)
                if slot in (23, 24, 25, 26, selected):
                    references.append({'pc': row['pc'], 'slot': int(slot), 'access': access, 'insideOwnRange': start <= row['pc'] < end})
    return {'entry': entry, 'startPc': start, 'endExclusivePc': end, 'bytes': 624, 'category': category, 'privateReturnPc': end - 4,
        'entryAliases': [entry], 'publicInteriorEntries': 0, 'sharedReturnTailDetected': False, 'knownIncomingReferences': incoming,
        'moduleGlobalSlots': [23, 24, 25, 26, selected], 'argumentBankLiveIns': [0, 1, 2, 3, 4], 'argumentBankCallClobbers': list(range(7)),
        'allKnownModuleGlobalReferences': references, 'privateLocalSlots': [], 'moduleAndArgumentObjectsAreNotPrivateLocals': True,
        'allOwnRecordPcs': [row['pc'] for row in own], 'followingPaddingRange': [end, end + 8], 'followingPaddingSourceCredit': 0,
        'opaqueNativeComputedReferenceCoverageComplete': False, 'naturalCallerReachabilityProven': False}


def build(data):
    rebuilt, records = bytearray(data['script']), []
    for unit in fixtures.UNITS:
        entry, start, end, category, unused = unit
        source = ROOT / 'src/scripts/20261030/batch19' / ('object' + str(category))
        directory = WORK / ('source-only-' + str(category))
        directory.mkdir(parents=True, exist_ok=True)
        filename = 'configure_primary_object' + str(category) + '.c'
        files = [(ROOT / name, name) for name in PIN_PATHS[:2]] + [(source / name, name) for name in (filename, 'scr_runtime_configuration.h', 'objects.bindings.json')]
        for path, name in files:
            shutil.copyfile(path, directory / name)
        command = [sys.executable, 'scr_c_compiler_20261030_v16.py', '--source', filename, '--base', str(start),
            '--bindings', 'objects.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json']
        result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        body = (directory / 'generated.scrfunc').read_bytes()
        assert body == data['code'][start:end] and len(body) == 624
        rebuilt[4100 + start:4100 + end] = body
        records.append({'entry': entry, 'range': {'startPc': start, 'endExclusivePc': end, 'bytes': 624, 'sha256': digest(body)},
            'command': command, 'cwd': str(directory), 'exitCode': result.returncode, 'inputs': [artifact(directory / name) for unused, name in files],
            'emittedBody': artifact(directory / 'generated.scrfunc'), 'compilerReport': artifact(directory / 'build.json'),
            'compilerEvidence': json.loads((directory / 'build.json').read_text()), 'originalBytecodeCompilerInput': False})
    assert rebuilt == data['script']
    output = WORK / 'world.source-runtime-configuration.scr'
    output.write_bytes(rebuilt)
    return bytes(rebuilt), {'units': records, 'rebuiltImage': artifact(output), 'originalBytecodeCompilerInput': False}


def controls():
    source = ROOT / 'src/scripts/20261030/batch19/object6'
    text = (source / 'configure_primary_object6.c').read_text()
    header = (source / 'scr_runtime_configuration.h').read_text()
    profile = json.loads((source / 'objects.bindings.json').read_text())
    alias, outside, argument = [json.loads(json.dumps(profile)) for unused in range(3)]
    alias['objects']['shared_parameter_first'] = {'bank': 0, 'slot': 24}
    outside['objects']['dispatch_argument0'] = {'bank': 1, 'slot': 16}
    argument['objects']['shared_parameter_first'] = {'bank': 1, 'slot': 7}
    tests = [('index1536', text.replace('get_primary_flag(configured_primary_6)', 'get_primary_flag(1536)'), header, profile),
        ('index_negative', text.replace('get_primary_flag(configured_primary_6)', 'get_primary_flag(-1)'), header, profile),
        ('argument_write', text, header, argument), ('aliased_objects', text, header, alias), ('argument_slot16', text, header, outside),
        ('category256', text, header.replace('object_category = 6', 'object_category = 256'), profile),
        ('wrong_API_type', text, header.replace('float selector);', 'int selector);'), profile),
        ('missing_object', text, header.replace('extern float dispatch_argument0;\n', ''), profile),
        ('unbound_source', text.replace('shared_parameter_first = dispatch_argument0;', 'shared_parameter_first = unknown;'), header, profile),
        ('wrong_arity', text.replace('shared_parameter_fourth, 0, -1', 'shared_parameter_fourth, 0'), header, profile)]
    output = []
    for name, code, declarations, bindings in tests:
        directory = ROOT / 'nonmatching/script-source/20261030/batch19-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / 'control.c'
        path.write_text(code)
        (directory / 'scr_runtime_configuration.h').write_text(declarations)
        try:
            compiler.compile_source(path, 11912, bindings)
        except ValueError as error:
            output.append({'name': name, 'source': artifact(path), 'header': artifact(directory / 'scr_runtime_configuration.h'),
                'bindings': bindings, 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Unsupported configuration source compiled: ' + name)
    return output


def main():
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    assert set(PINS) == set(PIN_PATHS) and all(digest((ROOT / name).read_bytes()) == pin for name, pin in PINS.items())
    data = assets.load(ROOT / 'extract/files/world.e')
    scope = [boundary(data, unit) for unit in fixtures.UNITS]
    rebuilt, source = build(data)
    rejected = controls()
    original = fixtures.run(data['script'])
    print(json.dumps({'stage': 'original configuration complete', 'returns': original['actualReturningCalls']}), flush=True)
    compiled = fixtures.run(rebuilt)
    assert original == compiled
    unused, files = assets.original_files()
    report = {'evidenceClass': 'ordinary-C-complete-shared-module-primary-configuration-SCR-source-match', 'generator': Path(__file__).name,
        'generatorSha256': digest(Path(__file__).read_bytes()), 'romSha256': assets.ROM_HASH, 'romFileRange': list(files['world.e']),
        'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
        'sourceClosure': [{'path': name, 'sha256': pin} for name, pin in PINS.items()], 'boundariesAndStorage': scope, 'sourceOnlyBuild': source,
        'compilerControls': rejected, 'differential': original, 'pairedCompleteOwnEntryExecutions': original['completeOwnEntryExecutions'] * 2,
        'pairedNativeReturningCalls': original['actualReturningCalls'] * 2, 'sourceDefinitionCount': 2, 'completeFunctionInstances': 2,
        'implementationFamilyCount': 1, 'qualifiedScriptRangeBytes': 1248, 'originalScaffoldingBytes': len(data['script']) - 1248,
        'scaffoldingSourceCredit': 0, 'nativeExecutableByteCredit': 0, 'completeImagesRecovered': 0, 'nativeFunctionStubs': 0,
        'postFaultStateUsedForProof': False, 'wholeRomSourceMatch': False, 'originalConstructorRetained': True,
        'constructorCapacityExhaustedReturnOnly': True, 'freePoolSuccessOrNaturalSceneReachabilityProven': False,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'sourceBytes': 1248, 'completeEntries': report['pairedCompleteOwnEntryExecutions'], 'nativeReturns': report['pairedNativeReturningCalls']}), flush=True)


if __name__ == '__main__':
    main()
