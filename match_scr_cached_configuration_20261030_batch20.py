import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/script-source/20261030/batch20/cached-configuration'
OUTPUT = ROOT / 'evidence/encounter/scripts-cached-configuration-contexts-20261030.json'
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
 'src/scripts/20261030/batch19/object7/objects.bindings.json': '5e4be97b1b42b13fb76f1ecede653ee117b0aad9ca7ba73d5382b0c67f1891a0',
 'match_scr_runtime_configuration_20261030_batch19.py': '0311afc386e8fd86a2a3685fd82b3a2b136f4dbb9f86961e703d5d5167cd90e8',
 'nonmatching/script-source/20261030/native_scr_cached_configuration_20261030.py': '36240750c3852d5b1c79355fa2942f2352434d742729e78150f4ea16ca8d97d2'}
sys.path[:0] = [str(ROOT / 'evidence/encounter'), str(ROOT / 'nonmatching/script-source/20261029'), str(ROOT / 'nonmatching/script-source/20261030')]
import script_assets_20261029 as assets
import native_scr_cached_configuration_20261030 as fixtures
import match_scr_runtime_configuration_20261030_batch19 as frozen
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def build(data):
    rebuilt, products = bytearray(data['script']), []
    for unit in fixtures.frozen.UNITS:
        entry, start, end, category, unused = unit
        source = ROOT / 'src/scripts/20261030/batch19' / ('object' + str(category))
        directory = WORK / ('source-only-' + str(category))
        directory.mkdir(parents=True, exist_ok=True)
        filename = 'configure_primary_object' + str(category) + '.c'
        inputs = [(ROOT / name, name) for name in ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261030_v16.py')]
        inputs += [(source / name, name) for name in (filename, 'scr_runtime_configuration.h', 'objects.bindings.json')]
        for path, name in inputs:
            shutil.copyfile(path, directory / name)
        command = [sys.executable, 'scr_c_compiler_20261030_v16.py', '--source', filename, '--base', str(start),
            '--bindings', 'objects.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json']
        result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        body = (directory / 'generated.scrfunc').read_bytes()
        assert body == data['code'][start:end] and len(body) == 624
        rebuilt[4100 + start:4100 + end] = body
        products.append({'entry': entry, 'startPc': start, 'endExclusivePc': end, 'bytes': len(body), 'sha256': digest(body),
            'inputs': [artifact(directory / name) for unused, name in inputs], 'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
            'emittedBody': artifact(directory / 'generated.scrfunc'), 'compilerReport': artifact(directory / 'build.json'),
            'compilerEvidence': json.loads((directory / 'build.json').read_text()), 'originalBytecodeCompilerInput': False})
    assert rebuilt == data['script']
    output = WORK / 'world.source-cached-configuration.scr'
    output.write_bytes(rebuilt)
    return bytes(rebuilt), {'units': products, 'rebuiltImage': artifact(output), 'reusedSourceBytes': 1248,
        'newSourceByteCredit': 0, 'newSourceDefinitionCredit': 0}


def main():
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    assert all(digest((ROOT / name).read_bytes()) == pin for name, pin in PINS.items())
    assert all(PINS[name] == value for name, value in frozen.PINS.items())
    assert fixtures.native.ROOT == ROOT
    assert all(digest(blob) == pin for blob, pin in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH),
        (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH), (fixtures.native.ITCM, fixtures.native.ITCM_HASH)))
    data = assets.load(ROOT / 'extract/files/world.e')
    rebuilt, products = build(data)
    original = fixtures.run(data['script'])
    print(json.dumps({'stage': 'original cache-qualified complete', 'returns': original['actualReturningCalls']}), flush=True)
    compiled = fixtures.run(rebuilt)
    assert original == compiled
    unsupported = fixtures.unsupported_cache_miss(data['script'])
    assert unsupported == fixtures.unsupported_cache_miss(rebuilt)
    rows = [part for case in original['cases'] for part in (case['first'], case['second'])]
    nested = sum(len(row['resourceCalls']) for row in rows) * 2
    report = {'evidenceClass': 'fresh-source-linked-existing-SCR-positive-record-allocation-cache-context-extension',
        'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'sourceClosure': [{'path': name, 'sha256': pin} for name, pin in PINS.items()], 'romSha256': assets.ROM_HASH,
        'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']),
        'nativeModuleHashes': {'main': fixtures.native.MAIN_HASH, 'overlay000': fixtures.native.OVERLAY_HASH, 'itcm': fixtures.native.ITCM_HASH},
        'nativeSourceRoot': str(fixtures.native.ROOT),
        'sourceOnlyBuild': products, 'boundariesAndStorage': [frozen.boundary(data, unit) for unit in fixtures.frozen.UNITS],
        'differential': original, 'unsupportedControls': [unsupported], 'pairedCompleteOwnEntryExecutions': original['completeOwnEntryExecutions'] * 2,
        'pairedNativeReturningCalls': original['actualReturningCalls'] * 2, 'pairedActualNestedResourceReturns': nested,
        'chosenRowCoverage': sorted({row['chosenFirstFreeRow'] for row in rows}),
        'nativeResourceReturnCoverage': sorted({entry['resultWord'] for row in rows for entry in row['resourceCalls']}),
        'nativePrimaryModeCoverage': [0, 2], 'originalConstructorAndResourceHelpersRetained': True, 'providerCount': 0,
        'recordAllocationDespiteResourceReturn0Observed': True, 'nativeAssetReadinessProven': False, 'naturalSceneOrAccessRenewalMeaningProven': False,
        'newSourceByteCredit': 0, 'newSourceDefinitionCredit': 0, 'newNativeByteCredit': 0, 'completeImageCredit': 0,
        'postFaultStateCredit': 0, 'wholeRomSourceMatch': False}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'completeEntries': report['pairedCompleteOwnEntryExecutions'], 'nativeReturns': report['pairedNativeReturningCalls'],
        'nestedResourceReturns': nested, 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
