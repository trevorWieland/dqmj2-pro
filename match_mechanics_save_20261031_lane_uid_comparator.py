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
    parser.add_argument('--source', default='src/mechanics_save/20261031_lane_uid_comparator/native_main_0207cc74.c')
    arguments = parser.parse_args()
    if Path(arguments.source).is_absolute() or '..' in Path(arguments.source).parts:
        raise AssertionError('Source must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python/Unicorn runtime is required')
    verify_inputs()
    script = 'evidence/application/save_core_comparator_fixtures_20261031.py'
    fixture_path = 'evidence/lanes/save-core/comparator-fixtures-20261031.json'
    command = [sys.executable, str(ROOT / script), '--source', arguments.source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    oracle = json.loads((ROOT / fixture_path).read_text())
    cache,entries,rows = {},{},[]
    for raw in oracle['matches']:
        row = dict(raw)
        row.update(row['realLinkSnapshot'])
        row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False,
            'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'})
        if row['sourceSha256'] != '3287271c5c394279c060553d3c2d8104f87853a7826fa53729b0c96c98685bf5':
            raise AssertionError('Audited source hash changed')
        if oracle['nativeCaseDigest'] != '8e50a8223fd924cacb9c2506825f62caff2c1e8f173dcd0e8c4c0dc12bd9dc6f':
            raise AssertionError('Native semantic vector identity changed')
        for dependency in oracle['runtimeDependencies']:
            if sha((ROOT / dependency['path']).read_bytes()) != dependency['sha256']:
                raise AssertionError('Current runtime dependency changed')
        if not row['exactByteEqual'] or row['compiledBytes'] != 144 or not dependencies_current(row):
            raise AssertionError('Complete source/closure did not match')
        for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
            ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
                raise AssertionError('Current source/object/real-link identity changed')
        address = int(row['address'],0)
        assert address == 0x0207CC74
        own = native_entry('main', address, cache)
        if row['nativeAlias'] != own['nativeAlias'] or row['bytes'] != own['bytes'] or own['bytes'] != 144:
            raise AssertionError('Own measured identity differs')
        metadata, binary, functions = cache['main']
        offset = address - int(metadata['base'], 0)
        native = binary[offset:offset + 144]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        if native != linked or len(linked) != 144 or validation.get('exactCallerBytes') is not True:
            raise AssertionError('Complete source/native/link bytes differ')
        if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
            raise AssertionError('Pinned real MW link did not succeed')
        if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
            raise AssertionError('Real link source/object differs')
        if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
            raise AssertionError('Real link native/source identity differs')
        row.update({'exactBytes':144,'exactAfterDeclaredRelocation':True,'exactAfterRealMwLink':True,
            'signature':f"s32 {row['name']}(const u32 *left, const u32 *right)",
            'oracle':{'supported':True,'cases':5691,'actualReturns':11382,'report':fixture_path,
                'reportSha256':sha((ROOT/fixture_path).read_bytes()),'limits':oracle['limits']}})
        entries[row['name']] = own
        for relocation in row['relocations']:
            module,target = relocation['targetModule'],int(relocation['target'],0)
            entries[relocation['symbol']] = data_entry(module,target,cache) if relocation['targetMode']=='data' else native_entry(module,target,cache)
        rows.append(row)
    assert len(rows)==1 and oracle['counts']['directContexts']==5691 and oracle['counts']['actualTopLevelReturns']==11426
    assert oracle['counts']['providers']==0 and oracle['counts']['unsupportedStops']==10
    for address in (0x02062A10,0x02044DC4,0x020449D4,0x0201D470,0x0207CA3C):
        entry = native_entry('main', address, cache)
        entries[entry['nativeAlias']] = entry
    control_script = 'evidence/application/save_core_comparator_controls_20261031.py'
    check = subprocess.run([sys.executable,str(ROOT/control_script)],capture_output=True,text=True,timeout=90)
    assert check.returncode==0, check.stdout+check.stderr
    controls_path = 'evidence/lanes/save-core/comparator-controls-20261031.json'
    controls = json.loads((ROOT/controls_path).read_text())
    assert controls['counts']==dict(nativeReturns=11,compiledWrongReturns=11,independentReturnRejections=5,positiveReturnControls=6,strictModelRejections=8,providers=0,sourceCredit=0)
    deps = [entry['path'] for entry in oracle['runtimeDependencies']]
    deps += [control_script,controls_path,*[row['source'] for row in controls['wholeSourceRealLinks']]]
    deps += [script, 'evidence/application/save_core_comparator_machine_20261031.py', 'evidence/application/save_core_comparator_build_20261031.py',
        'match_mechanics_save_20261031_lane_uid_comparator.py', 'provenance/seed-manifest.json',
        'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py', 'source_dependencies.py']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': rows, 'matchedFunctions': 1, 'matchedBytes': 144,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': len(oracle['vectors']), 'actualReturns': oracle['counts']['actualTopLevelReturns'],
            'counts':oracle['counts'],
            'providers': oracle['counts']['providers'],
            'providerKinds': 0,
            'nativeCaseDigest': oracle['nativeCaseDigest'],
            'reports': [x['oracle'] for x in rows], 'reproductionCommands': [command]},
        'replayRequires': [], 'negativeControls':{'report':controls_path,'sha256':sha((ROOT/controls_path).read_bytes()),'counts':controls['counts']},
        'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
        'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261031-lane-uid-comparator.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 1, 'matchedBytes': 144, 'cases': len(oracle['vectors']),
        'actualReturns': oracle['counts']['actualTopLevelReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
