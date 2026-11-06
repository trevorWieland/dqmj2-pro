import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, native_entry, ROM_SHA, SAVE_SHA, MAIN_SHA
from source_dependencies import dependencies_current


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-directory', default='src/mechanics_save/20261030_footer_wrappers')
    args = parser.parse_args()
    assert not Path(args.source_directory).is_absolute() and '..' not in Path(args.source_directory).parts
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    script = 'evidence/application/footer_wrapper_abi_fixtures_20261030.py'
    fixture = 'evidence/application/footer-wrapper-abi-fixtures-20261030.json'
    command = [sys.executable, str(ROOT / script), '--source-directory', args.source_directory]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    assert process.returncode == 0, process.stdout + process.stderr
    oracle = json.loads((ROOT / fixture).read_text())
    assert oracle['counts'] == {'contexts': 108, 'actualWrapperReturns': 216,
        'actualOriginalTailLeafReturns': 216, 'unsupportedStops': 8, 'providers': 0}
    source_pins = {'native_main_0206be08': '7a6bc3b82e2aaf81e8daf1e83287c8d960c48f7e1aefdfedd060b9eecad6165a', 'native_main_0206be14': 'fda8e445ce3aee5233af4eabe50d5827f49e3a2be51eccbeea8507f934d56ca1'}
    legacy = {'src/runtime/runtime09/native_main_0206be08.c': 'fdc1ffc0fb206b2d7770fe74b9ebe157c38d7b54c48d0830bbaef4438c30c971',
        'src/runtime/runtime09/native_main_0206be14.c': '21401c94853ffb47804191392fce2ad133903e3498592c797ab781fe5e6832cd'}
    assert oracle['nativeCaseDigest'] == '60789dae84970c0bb11115d5e48ec11abfbcbbc1f4a64bde5cfb3838cf6aecc9'
    cache, entries, matches = {}, {}, []
    for candidate in oracle['candidates']:
        row = dict(candidate)
        row.update(row['realLinkSnapshot'])
        address = int(row['address'], 0)
        assert row['sourceSha256'] == source_pins[row['name']]
        assert row['exactByteEqual'] and row['compiledBytes'] == 12 and dependencies_current(row)
        for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'), ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT / row[path_key]).read_bytes()) == row[hash_key]
        own = native_entry('main', address, cache)
        assert own['bytes'] == 12 and row['nativeAlias'] == own['nativeAlias']
        metadata, binary, functions = cache['main']
        offset = address - int(metadata['base'], 0)
        native = binary[offset:offset + 12]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        assert native == linked and len(linked) == 12 and validation.get('exactCallerBytes') is True
        assert validation['sourceSha256'] == row['sourceSha256'] and validation['sourceObjectSha256'] == row['objectSha256']
        assert validation['linkerAttempt']['exitCode'] == 0 and validation['linkerSha256'] == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        vectors = [vector for vector in oracle['vectors'] if int(vector['entry'], 0) == address]
        signature = 'u32 native_main_0206be08(u32 index, u32 value)' if address == 0x0206BE08 else 'u32 native_main_0206be14(u32 index)'
        row.update({'exactBytes': 12, 'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
            'outputSha256': sha(linked), 'linked': False, 'signature': signature,
            'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe', 'netNewSourceBytes': 0,
            'oracle': {'supported': True, 'cases': len(vectors), 'actualReturns': len(vectors) * 2,
                'report': fixture, 'reportSha256': sha((ROOT / fixture).read_bytes()), 'limits': oracle['limits']}})
        entries[row['name']] = own
        for relocation in row['relocations']:
            assert relocation['targetMode'] != 'data'
            entries[relocation['symbol']] = native_entry(relocation['targetModule'], int(relocation['target'], 0), cache)
        matches.append(row)
    for path, expected in legacy.items():
        assert sha((ROOT / path).read_bytes()) == expected
    deps = [entry['path'] for entry in oracle['runtimeDependencies']]
    for entry in oracle['runtimeDependencies']:
        assert sha((ROOT / entry['path']).read_bytes()) == entry['sha256']
    deps += [script, 'evidence/application/footer_wrapper_abi_build_20261030.py',
        'match_mechanics_save_20261030_footer_wrapper_abi.py', 'match_mechanics_save_20261029_record33.py',
        'source_dependencies.py', 'provenance/seed-manifest.json']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': matches, 'matchedFunctions': 2, 'matchedBytes': 24, 'netNewMatchedFunctions': 0, 'netNewMatchedBytes': 0,
        'sourceCorrectnessAlternatives': True, 'retainedLegacyParameterContracts': legacy,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'sourceDependencies': [{'path': path, 'sha256': digest} for path, digest in legacy.items()],
        'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': 108, 'actualReturns': 216, 'actualOriginalTailLeafReturns': 216,
            'prototypeProbes': oracle['prototypeProbes'], 'nativeCaseDigest': oracle['nativeCaseDigest'],
            'reproductionCommands': [command]}, 'wholeLinkedRebuild': False,
        'registrationPerformedByThisScript': False, 'inputsUnchanged': True, 'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261030-footer-wrapper-abi.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 2, 'matchedBytes': 24, 'netNewMatchedBytes': 0,
        'actualReturns': 216, 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
