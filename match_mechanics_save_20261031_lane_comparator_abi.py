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
    parser.add_argument('--source-directory', default='src/mechanics_save/20261031_lane_comparator_abi')
    arguments = parser.parse_args()
    if Path(arguments.source_directory).is_absolute() or '..' in Path(arguments.source_directory).parts:
        raise AssertionError('Source must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python/Unicorn runtime is required')
    verify_inputs()
    script = 'evidence/application/save_core_comparator_abi_fixtures_20261031.py'
    fixture_path = 'evidence/lanes/save-core/comparator-abi-fixtures-20261031.json'
    command = [sys.executable, str(ROOT / script), '--source-directory', arguments.source_directory]
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
        if row['sourceSha256'] not in ['177dcf35c8d0f57559e96d4145154986f7c456084ff29088eb7a10b511012c8b', '8405ce718015aa580da49c8b3b36499ba8506c1c8d2a63e60ce2060af0f65429', 'ff529f42481807db77b2c9c51125c4f7b148e7029a88fdc6b727349301b8c0e8']:
            raise AssertionError('Audited source hash changed')
        if oracle['nativeCaseDigest'] != 'f118f2e39f47e5b0330d253adf4aa9a439f814963c5c56e337d54303ba98eec1':
            raise AssertionError('Native semantic vector identity changed')
        for dependency in oracle['runtimeDependencies']:
            if sha((ROOT / dependency['path']).read_bytes()) != dependency['sha256']:
                raise AssertionError('Current runtime dependency changed')
        if not row['exactByteEqual'] or row['compiledBytes'] != row['bytes'] or not dependencies_current(row):
            raise AssertionError('Complete source/closure did not match')
        for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
            ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
                raise AssertionError('Current source/object/real-link identity changed')
        address = int(row['address'],0)
        assert address in (0x0207CB3C,0x0207CBEC,0x0207CD04)
        own = native_entry('main', address, cache)
        if row['nativeAlias'] != own['nativeAlias'] or row['bytes'] != own['bytes'] or own['bytes'] != row['compiledBytes']:
            raise AssertionError('Own measured identity differs')
        metadata, binary, functions = cache['main']
        offset = address - int(metadata['base'], 0)
        native = binary[offset:offset + row['compiledBytes']]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        if native != linked or len(linked) != row['compiledBytes'] or validation.get('exactCallerBytes') is not True:
            raise AssertionError('Complete source/native/link bytes differ')
        if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
            raise AssertionError('Pinned real MW link did not succeed')
        if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
            raise AssertionError('Real link source/object differs')
        if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
            raise AssertionError('Real link native/source identity differs')
        measured_counts = next(x for x in oracle['perFunctionCounts'] if int(x['entry'],0)==address)
        row.update({'exactBytes':row['compiledBytes'],'exactAfterDeclaredRelocation':True,'exactAfterRealMwLink':True,
            'signature':f"s32 {row['name']}(const u32 *left, const u32 *right)",
            'oracle':{'supported':True,'cases':measured_counts['directContexts']+measured_counts['sortContexts'],'actualReturns':measured_counts['actualTopReturns'],'counts':measured_counts,'report':fixture_path,
                'reportSha256':sha((ROOT/fixture_path).read_bytes()),'limits':oracle['limits']}})
        entries[row['name']] = own
        for relocation in row['relocations']:
            module,target = relocation['targetModule'],int(relocation['target'],0)
            entries[relocation['symbol']] = data_entry(module,target,cache) if relocation['targetMode']=='data' else native_entry(module,target,cache)
        rows.append(row)
    assert len(rows)==3 and oracle['counts']['contexts']==4887 and oracle['counts']['actualTopReturns']==9774
    assert oracle['counts']['providers']==0 and oracle['counts']['unsupportedStops']==36
    for address in (0x02062A10,0x02044CDC,0x020449D4,0x0201D470,0x0207CA3C):
        entry = native_entry('main', address, cache)
        entries[entry['nativeAlias']] = entry
    control_script = 'evidence/application/save_core_comparator_abi_controls_20261031.py'
    check = subprocess.run([sys.executable,str(ROOT/control_script)],capture_output=True,text=True,timeout=90)
    assert check.returncode==0, check.stdout+check.stderr
    controls_path = 'evidence/lanes/save-core/comparator-abi-controls-20261031.json'
    controls = json.loads((ROOT/controls_path).read_text())
    assert controls['counts']==dict(nativeReturns=18,compiledWrongReturns=18,independentReturnRejections=9,positiveReturnControls=9,providers=0,netNewExecutableBytes=0)
    deps = [entry['path'] for entry in oracle['runtimeDependencies']]
    deps += [*[x['source'] for x in oracle['previousPrimaries']],control_script,controls_path,*[row['source'] for row in controls['wholeSourceRealLinks']]]
    deps += [script, 'evidence/application/save_core_comparator_abi_machine_20261031.py', 'evidence/application/save_core_comparator_abi_build_20261031.py',
        'match_mechanics_save_20261031_lane_comparator_abi.py', 'provenance/seed-manifest.json',
        'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py', 'source_dependencies.py']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': rows, 'matchedFunctions': 3, 'matchedBytes': 460, 'netNewExecutableBytes':0,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': len(oracle['vectors']), 'actualReturns': oracle['counts']['actualTopReturns'],
            'counts':oracle['counts'],
            'providers': oracle['counts']['providers'],
            'providerKinds': 0,
            'nativeCaseDigest': oracle['nativeCaseDigest'],
            'reports': [x['oracle'] for x in rows], 'reproductionCommands': [command]},
        'migration':{'zeroNewCoverage':True,'previousPrimaries':oracle['previousPrimaries'],'acceptedOriginalsUntouched':True},
        'replayRequires': [], 'negativeControls':{'report':controls_path,'sha256':sha((ROOT/controls_path).read_bytes()),'counts':controls['counts']},
        'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
        'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261031-lane-comparator-abi.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 3, 'matchedBytes': 460, 'netNewExecutableBytes':0, 'cases': len(oracle['vectors']),
        'actualReturns': oracle['counts']['actualTopReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
