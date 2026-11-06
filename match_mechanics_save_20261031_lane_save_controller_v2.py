import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,native_entry,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current

CASE_DIGEST = '04791ef813c61bfda196f109685935a7beda62fc180a01b11db6dc05a58da6ff'
FIXTURE = 'evidence/application/save_core_controller_fixtures_20261031_v2.py'
ORACLE = 'evidence/application/save-core-controller-source-20261031-v2.json'
CONTROL_SCRIPT = 'evidence/application/save_core_controller_controls_20261031_v2.py'
CONTROLS = 'evidence/lanes/save-core/save-controller-controls-20261031-v2.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source',default='src/mechanics_save/20261031_lane_save_controller/native_main_02079170.c')
    args = parser.parse_args()
    assert not Path(args.source).is_absolute() and '..' not in Path(args.source).parts
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs()
    command = [sys.executable,str(ROOT/FIXTURE),'--source',args.source]
    for cmd in (command,[sys.executable,str(ROOT/CONTROL_SCRIPT)]):
        process = subprocess.run(cmd,capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    oracle = json.loads((ROOT/ORACLE).read_text())
    controls = json.loads((ROOT/CONTROLS).read_text())
    assert oracle['nativeCaseDigest']==CASE_DIGEST
    assert oracle['counts']['controllerContexts']==2099 and oracle['counts']['actualControllerReturns']==4140
    assert oracle['counts']['directPrimitiveContexts']==1040 and oracle['counts']['actualDirectPrimitiveReturns']==2080
    assert controls['counts']['independentRejections']==14 and controls['counts']['positiveControls']==4
    assert controls['counts']['nativeReturns']==18 and controls['counts']['compiledWrongReturns']==18
    assert controls['counts']['cleanupContractRejections']==4 and controls['counts']['cleanupContractPositiveControls']==1
    cache,entries,rows = {},{},[]
    for raw in oracle['matches']:
        row = dict(raw)
        row.update(row['realLinkSnapshot'])
        row.update(outputSha256=row['linkedBinarySha256'],linked=False)
        assert row['exactByteEqual'] and row['compiledBytes']==row['bytes'] and dependencies_current(row)
        for path_key,hash_key in [('source','sourceSha256'),('object','objectSha256'),
            ('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT/row[path_key]).read_bytes())==row[hash_key]
        address,length = int(row['address'],0),row['bytes']
        own = native_entry('main',address,cache)
        assert row['nativeAlias']==own['nativeAlias'] and length==own['bytes']
        metadata,binary,functions = cache['main']
        offset = address-int(metadata['base'],0)
        native,linked = binary[offset:offset+length],(ROOT/row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert native==linked and len(linked)==length and validation['exactCallerBytes'] is True
        assert validation['linkerAttempt']['exitCode']==0 and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256']
        assert validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        case_count = 2099 if address==0x02079170 else sum(int(v['entry'],0)==address for v in oracle['directPrimitiveVectors'])
        if row['zeroCoverageAbiReplacement']:
            previous = f'src/runtime/runtime06/native_main_{address:08x}.c'
            row.update(previousSource=previous,previousSourceSha256=sha((ROOT/previous).read_bytes()),zeroNewCoverage=True)
        row.update(exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            signature=('u32 '+row['name']+'(void)') if address==0x02079170 else
                ('s32 '+row['name']+'(void)') if row['zeroCoverageAbiReplacement'] else ('void '+row['name']+'(s32)'),
            oracle=dict(supported=True,cases=case_count,
                actualReturns=4140 if address==0x02079170 else 2*case_count,
                controlledBoundaryStops=58 if address==0x02079170 else 0,
                report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limits']))
        entries[row['name']] = own
        for relocation in row['relocations']:
            module,target = relocation['targetModule'],int(relocation['target'],0)
            entries[relocation['symbol']] = data_entry(module,target,cache) if relocation['targetMode']=='data' else native_entry(module,target,cache)
        rows.append(row)
    assert len(rows)==5 and sum(row['bytes'] for row in rows)==1420
    for dependency in oracle['nativeDependencies']:
        own = native_entry(dependency['module'],int(dependency['address'],0),cache)
        entries[own['nativeAlias']] = own
    for contract in oracle['qualifiedCalleeContracts']:
        assert sha((ROOT/contract['source']).read_bytes())==contract['sha256']
        assert contract['sha256']=='4891fe1173faae2c3450539593b70f2e0f018da5928464eeb23a0e454dfd4169'
    for contract in oracle['providerContracts']:
        own = native_entry(contract['module'],int(contract['address'],0),cache)
        entries[own['nativeAlias']] = own
    for dependency in oracle['runtimeDependencies']:
        assert sha((ROOT/dependency['path']).read_bytes())==dependency['sha256']
    deps = [d['path'] for d in oracle['runtimeDependencies']]
    deps += [FIXTURE,CONTROL_SCRIPT,CONTROLS,'evidence/application/save_core_controller_machine_20261031_v2.py',
        'evidence/application/save_core_controller_model_20261031_v2.py','evidence/application/save_core_controller_build_20261031.py',
        'match_mechanics_save_20261031_lane_save_controller_v2.py','provenance/seed-manifest.json',
        'match_mechanics_save_20261029_record33.py','match_mechanics_save_20261029_item_use.py','source_dependencies.py']
    deps += [row['source'] for row in rows]+[row['source'] for row in controls['wholeSourceRealLinks']]
    deps += [controls['legacyAbiAudit']['source']]+[d['path'] for d in controls['legacyAbiAudit']['legacyWrapperSources']]
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    deps += [contract['source'] for contract in oracle['qualifiedCalleeContracts']]
    verify_inputs()
    report = dict(schemaVersion=2,qualifiedCalleeContracts=oracle['qualifiedCalleeContracts'],providerContracts=oracle['providerContracts'],romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,
        matches=rows,matchedFunctions=5,matchedBytes=1420,newCoverageFunctions=3,newCoverageBytes=1380,
        abiReplacementFunctions=2,abiReplacementBytes=40,
        nativeSymbolEntries=entries,nativeSymbols={n:e['address'] for n,e in entries.items()},
        nativeSymbolModules={n:e['module'] for n,e in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(set(deps))],
        oracle=dict(cases=3139,controllerCases=2099,directPrimitiveCases=1040,actualReturns=6220,controlledBoundaryStops=58,counts=oracle['counts'],
            providedCalls=oracle['counts']['substitutedBoundaryCompletions'],
            providerKinds=oracle['counts']['substitutedBoundaryKinds'],nativeCaseDigest=CASE_DIGEST,
            reports=[r['oracle'] for r in rows],reproductionCommands=[command]),
        replayRequires=[],negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts']),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limits'])
    target = ROOT/'evidence/matches/mechanics-save-20261031-lane-save-controller-v2.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(newFunctions=3,newBytes=1380,zeroCoverageMigrations=2,
        actualReturns=6220,controlledBoundaryStops=58,reportSha256=sha(target.read_bytes()))))


if __name__=='__main__':
    main()
