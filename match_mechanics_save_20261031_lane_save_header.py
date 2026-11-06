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
    parser.add_argument('--source', default='src/mechanics_save/20261031_lane_save_header/native_main_0207979c.c')
    arguments = parser.parse_args()
    if Path(arguments.source).is_absolute() or '..' in Path(arguments.source).parts:
        raise AssertionError('Source must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python/Unicorn runtime is required')
    verify_inputs()
    script = 'evidence/application/save_core_save_header_fixtures_20261031.py'
    fixture_path = 'evidence/lanes/save-core/save-header-fixtures-20261031.json'
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
        if row['sourceSha256'] != 'f9a3a608acaceaa7b4c02231f3af634e86ccc4dc2ca669e85ce96997731de5be':
            raise AssertionError('Audited source hash changed')
        if oracle['nativeCaseDigest'] != 'f90c113f95572e3ff610099388a956106deb61632d184dd8154fe1e8831f60f1':
            raise AssertionError('Native semantic vector identity changed')
        for dependency in oracle['runtimeDependencies']:
            if sha((ROOT / dependency['path']).read_bytes()) != dependency['sha256']:
                raise AssertionError('Current runtime dependency changed')
        if not row['exactByteEqual'] or row['compiledBytes'] != 100 or not dependencies_current(row):
            raise AssertionError('Complete source/closure did not match')
        for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
            ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
                raise AssertionError('Current source/object/real-link identity changed')
        address = int(row['address'],0)
        assert address == 0x0207979C
        own = native_entry('main', address, cache)
        if row['nativeAlias'] != own['nativeAlias'] or row['bytes'] != own['bytes'] or own['bytes'] != 100:
            raise AssertionError('Own measured identity differs')
        metadata, binary, functions = cache['main']
        offset = address - int(metadata['base'], 0)
        native = binary[offset:offset + 100]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        if native != linked or len(linked) != 100 or validation.get('exactCallerBytes') is not True:
            raise AssertionError('Complete source/native/link bytes differ')
        if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
            raise AssertionError('Pinned real MW link did not succeed')
        if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
            raise AssertionError('Real link source/object differs')
        if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
            raise AssertionError('Real link native/source identity differs')
        row.update({'exactBytes':100,'exactAfterDeclaredRelocation':True,'exactAfterRealMwLink':True,
            'signature':f"u32 {row['name']}(void)",
            'oracle':{'supported':True,'cases':584,'actualReturns':1168,'report':fixture_path,
                'reportSha256':sha((ROOT/fixture_path).read_bytes()),'limits':oracle['limits']}})
        entries[row['name']] = own
        for relocation in row['relocations']:
            module,target = relocation['targetModule'],int(relocation['target'],0)
            entries[relocation['symbol']] = data_entry(module,target,cache) if relocation['targetMode']=='data' else native_entry(module,target,cache)
        rows.append(row)
    assert len(rows)==1 and oracle['counts']['contexts']==584 and oracle['counts']['actualWrapperReturns']==1168
    assert oracle['counts']['providerKinds']==1 and oracle['counts']['modeledBankBlockReads']==1168
    for address in (0x0207DF2C,0x0207DAA0,0x02008E0C,0x02027D8C):
        entry = native_entry('main', address, cache)
        entries[entry['nativeAlias']] = entry
    control_script = 'evidence/application/save_core_save_header_controls_20261031.py'
    check = subprocess.run([sys.executable,str(ROOT/control_script)],capture_output=True,text=True,timeout=90)
    assert check.returncode==0, check.stdout+check.stderr
    controls_path = 'evidence/lanes/save-core/save-header-controls-20261031.json'
    controls = json.loads((ROOT/controls_path).read_text())
    assert controls['counts']==dict(nativeReturns=6,compiledWrongReturns=6,independentStateReturnRejections=3,positiveStateReturnControls=3,providerKinds=1,sourceCredit=0)
    deps = [entry['path'] for entry in oracle['runtimeDependencies']]
    deps += [control_script,controls_path,*[row['source'] for row in controls['wholeSourceRealLinks']]]
    deps += [d['path'] for row in controls['wholeSourceRealLinks'] for d in row['sourceDependencies']]
    deps += ['evidence/application/save_header_wrapper_source_20261030.py','evidence/application/save_header_wrapper_machine_20261030.py',
        'evidence/application/save_operations_virtual_20261030.py','evidence/application/save_operations_build_20261030.py']
    deps += [script, 'evidence/application/save_core_save_header_machine_20261031.py', 'evidence/application/save_core_save_header_build_20261031.py',
        'match_mechanics_save_20261031_lane_save_header.py', 'provenance/seed-manifest.json',
        'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py', 'source_dependencies.py']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': rows, 'matchedFunctions': 1, 'matchedBytes': 100,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': len(oracle['vectors']), 'actualReturns': oracle['counts']['actualWrapperReturns'],
            'counts':oracle['counts'],
            'providedCalls': oracle['counts']['modeledBankBlockReads'],
            'providerKinds': 1,
            'nativeCaseDigest': oracle['nativeCaseDigest'],
            'reports': [x['oracle'] for x in rows], 'reproductionCommands': [command]},
        'replayRequires': [], 'negativeControls':{'report':controls_path,'sha256':sha((ROOT/controls_path).read_bytes()),'counts':controls['counts']},
        'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
        'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261031-lane-save-header.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 1, 'matchedBytes': 100, 'cases': len(oracle['vectors']),
        'actualReturns': oracle['counts']['actualWrapperReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
