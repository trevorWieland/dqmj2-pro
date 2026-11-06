import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, native_entry, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='src/mechanics_save/20261030_footer_sentinel/native_main_02072b00.c')
    args = parser.parse_args()
    assert not Path(args.source).is_absolute() and '..' not in Path(args.source).parts
    import unicorn
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    verify_inputs()
    script = 'evidence/application/footer_sentinel_fixtures_20261030.py'
    fixture = 'evidence/application/footer-sentinel-fixtures-20261030.json'
    command = [sys.executable, str(ROOT / script), '--source', args.source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    assert process.returncode == 0, process.stdout + process.stderr
    oracle = json.loads((ROOT / fixture).read_text())
    assert oracle['counts'] == {'contexts': 1600, 'actualTopLevelReturns': 3200,
        'actualNativeHelperReturnScopes': 4800, 'aliasContexts': 320,
        'unsupportedStops': 6, 'providers': 0, 'writeOrderDifferences': 0}
    assert oracle['nativeCaseDigest'] == '19c8b03b3ab7db617e7fd5685d6de30aeaf053f1c356bd25cb85a14357a3fcc5'
    row = dict(oracle['candidate'])
    row.update(row['realLinkSnapshot'])
    assert row['sourceSha256'] == 'e945a6f0d61d05f14b8fe521bcec3fec76cf807527419ef89ac5872460e10fc9'
    assert row['exactByteEqual'] and row['compiledBytes'] == 116 and dependencies_current(row)
    for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
        ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
        ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        assert sha((ROOT / row[path_key]).read_bytes()) == row[hash_key]
    cache = {}
    own = native_entry('main', 0x02072B00, cache)
    assert own['bytes'] == 116 and row['nativeAlias'] == own['nativeAlias'] and row['bytes'] == 116
    metadata, binary, functions = cache['main']
    offset = 0x02072B00 - int(metadata['base'], 0)
    native = binary[offset:offset + 116]
    linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
    validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
    assert native == linked and len(linked) == 116 and validation.get('exactCallerBytes') is True
    assert validation['sourceSha256'] == row['sourceSha256'] and validation['sourceObjectSha256'] == row['objectSha256']
    assert validation['linkerAttempt']['exitCode'] == 0 and validation['linkerSha256'] == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
    assert validation['nativeSpanSha256'] == sha(native) and validation['linkedCallerSha256'] == sha(linked)
    row.update({'exactBytes': 116, 'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
        'outputSha256': sha(linked), 'linked': False, 'signature': 'u32 native_main_02072b00(Selection *selection)',
        'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe',
        'oracle': {'supported': True, 'cases': 1600, 'actualReturns': 3200,
            'report': fixture, 'reportSha256': sha((ROOT / fixture).read_bytes()), 'limits': oracle['limits']}})
    entries = {row['name']: own}
    for relocation in row['relocations']:
        module, target = relocation['targetModule'], int(relocation['target'], 0)
        entries[relocation['symbol']] = data_entry(module, target, cache) if relocation['targetMode'] == 'data' else native_entry(module, target, cache)
    deps = [entry['path'] for entry in oracle['runtimeDependencies']]
    for entry in oracle['runtimeDependencies']:
        assert sha((ROOT / entry['path']).read_bytes()) == entry['sha256']
    deps += [script, 'evidence/application/footer_sentinel_build_20261030.py',
        'match_mechanics_save_20261030_footer_sentinel.py', 'provenance/seed-manifest.json',
        'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py', 'source_dependencies.py']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': [row], 'matchedFunctions': 1, 'matchedBytes': 116,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': 1600, 'actualReturns': 3200, 'actualNativeHelperReturnScopes': 4800,
            'providers': 0, 'providerKinds': 0, 'nativeCaseDigest': oracle['nativeCaseDigest'],
            'reports': [row['oracle']], 'reproductionCommands': [command]},
        'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False,
        'inputsUnchanged': True, 'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261030-footer-sentinel.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 1, 'matchedBytes': 116, 'actualReturns': 3200,
        'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
