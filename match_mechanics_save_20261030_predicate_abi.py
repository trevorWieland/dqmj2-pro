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

PINS = {0x02072F48: (40, 'd6a8593201308390f013358cdb2df4b99ba6ba01c33c138ff1462484e54d766a', 'u32 native_main_02072f48(s32 species)'),
    0x0203D128: (16, 'affe4a58ded412054c18719e3c92393df2eeb5b2edf58d0e281d4d734e4d10e7', 'u32 native_main_0203d128(void)')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-directory', default='src/mechanics_save/20261030_predicate_abi')
    args = parser.parse_args()
    if Path(args.source_directory).is_absolute() or '..' in Path(args.source_directory).parts:
        raise AssertionError('Source directory must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python/Unicorn runtime is required')
    verify_inputs()
    script = 'evidence/application/predicate_abi_fixtures_20261030.py'
    fixture = 'evidence/application/predicate-abi-fixtures-20261030.json'
    command = [sys.executable, str(ROOT / script), '--source-directory', args.source_directory]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    oracle = json.loads((ROOT / fixture).read_text())
    if oracle['counts']['cases'] != 1040 or oracle['counts']['actualTopLevelReturns'] != 2080:
        raise AssertionError('Actual native/source case coverage changed')
    cache, entries, rows = {}, {}, []
    for candidate in oracle['candidates']:
        row = dict(candidate)
        row.update(row['realLinkSnapshot'])
        row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False,
            'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'})
        address = int(row['address'], 0)
        length, source_sha, signature = PINS[address]
        if row['sourceSha256'] != source_sha or row['compiledBytes'] != length or not row['exactByteEqual'] or not dependencies_current(row):
            raise AssertionError('Complete typed source/closure did not match')
        for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'), ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
                raise AssertionError('Current source/object/real-link identity changed')
        own = native_entry('main', address, cache)
        if row['nativeAlias'] != own['nativeAlias'] or row['bytes'] != length or own['bytes'] != length:
            raise AssertionError('Own measured identity differs')
        metadata, binary, functions = cache['main']
        offset = address - int(metadata['base'], 0)
        native = binary[offset:offset + length]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        if native != linked or len(linked) != length or validation.get('exactCallerBytes') is not True:
            raise AssertionError('Complete source/native/link bytes differ')
        if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
            raise AssertionError('Pinned real MW link did not succeed')
        if validation['sourceSha256'] != source_sha or validation['sourceObjectSha256'] != row['objectSha256']:
            raise AssertionError('Real link source/object differs')
        if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
            raise AssertionError('Real link native/source identity differs')
        cases = sum(sum(event['entry'] == hex(address) for event in vector['nativeHelperReturns']) for vector in oracle['vectors'])
        row.update({'exactBytes': length, 'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
            'signature': signature, 'netNewCoverageBytes': 0, 'primaryMigrationCandidate': True,
            'oracle': {'supported': True, 'cases': cases, 'actualReturns': 2 * cases, 'report': fixture,
                'reportSha256': sha((ROOT / fixture).read_bytes()), 'limits': oracle['limits']}})
        rows.append(row)
        entries[row['name']] = own
        for relocation in row['relocations']:
            module, target = relocation['targetModule'], int(relocation['target'], 0)
            entries[relocation['symbol']] = data_entry(module, target, cache) if relocation['targetMode'] == 'data' else native_entry(module, target, cache)
    if sorted(PINS) != sorted(int(row['address'], 0) for row in rows):
        raise AssertionError('Typed source set changed')
    expected_controls = [False, True, False, True]
    if [row['compilerAccepted'] for row in oracle['declarationControls']] != expected_controls:
        raise AssertionError('Declaration rejection controls changed')
    deps = [script, 'evidence/application/predicate_abi_build_20261030.py',
        'evidence/application/record_lookup_abi_machine_20261030.py',
        'evidence/application/roster-current-uid-arm7-20261030.py',
        'evidence/application/roster-collector-callers-arm7-20261030-setup.py',
        'evidence/application/roster-collectors-arm7-20261030.py',
        'evidence/application/allocation-constructor-other-modes-arm7-20261030.py',
        'evidence/application/allocation-constructor-arm7-20261030-setup.py',
        'evidence/application/allocation-constructor-arm7-20261030.py',
        'evidence/application/preparation_machine_20261029.py', 'evidence/application/eligibility_machine_20261029.py',
        'preparation_build_20261029.py', 'match_mechanics_save_20261029_record33.py',
        'match_mechanics_save_20261029_item_use.py', 'match_mechanics_save_20261030_predicate_abi.py',
        'link_runtime_unit.py', 'save_link_snapshots.py', 'source_dependencies.py', 'provenance/seed-manifest.json']
    deps += [item['source'] for item in oracle['declarationControls']]
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': rows, 'matchedFunctions': 2, 'matchedBytes': 56, 'netNewFunctions': 0, 'netNewBytes': 0,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': oracle['counts']['cases'], 'actualReturns': oracle['counts']['actualTopLevelReturns'],
            'reports': [row['oracle'] for row in rows], 'reproductionCommands': [command],
            'nativeCaseDigest': oracle['nativeCaseDigest'], 'declarationControls': oracle['declarationControls']},
        'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
        'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261030-predicate-abi.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 2, 'matchedBytes': 56, 'netNewBytes': 0,
        'actualReturns': oracle['counts']['actualTopLevelReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
