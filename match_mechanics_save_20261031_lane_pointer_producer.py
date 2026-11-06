import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261029_item_use import data_entry
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from source_dependencies import dependencies_current
FIXTURE='evidence/application/save_core_pointer_producer_fixtures_20261031.py'
ORACLE='evidence/application/save-core-pointer-producer-source-20261031.json'
CONTROL_SCRIPT='evidence/application/save_core_pointer_producer_controls_20261031.py'
CONTROLS='evidence/lanes/save-core/pointer-producer-controls-20261031.json'
CASE_DIGEST='9b334addf28bbbc609397f29e6009739d5986775190ca9385895628836430c4e'
WRAPPER_DIGEST='2a45452327c3050313479924d1aa74bcff52eb1e2aafc30dade88f124daff4b0'
CONTROL_DIGEST='735231cc12f3feb33c2330d6d46df06de46a22249bb1f9f2bc8df011aa76464e'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs()
    commands=[[sys.executable,str(ROOT/p)] for p in (FIXTURE,CONTROL_SCRIPT)]
    for cmd in commands:
        process=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text())
    controls=json.loads((ROOT/CONTROLS).read_text())
    assert oracle['counts']['directContexts']==1412 and oracle['counts']['actualEntryReturns']==2824
    assert oracle['counts']['actualWrapperReturns']==1952 and oracle['counts']['actualHelperReturns']==21264
    assert oracle['counts']['explicitHostModeWrites']==576 and oracle['counts']['providers']==0
    vectors=unpack(oracle['vectorSidecar'],CASE_DIGEST)
    wrappers=unpack(oracle['wrapperSidecar'],WRAPPER_DIGEST)
    negatives=unpack(controls['vectorSidecar'],CONTROL_DIGEST)
    assert len(vectors)==1412 and len(wrappers)==976
    assert all(v['result']['actualReturn'] for v in vectors) and all(v['actualReturn'] for v in wrappers)
    assert len(negatives)==72 and sum(v['independentEffectRejected'] for v in negatives)==18
    assert sum(v['readPatternMismatch'] for v in negatives)==60
    assert all(v['native']['actualReturn'] and v['nonvolatileC']['actualReturn'] for v in negatives)
    failures={v['kind']:(v['failure'],v['pc']) for v in oracle['unsupported']}
    assert failures=={'producer-write':('PointerSequenceWriteBounds','0x209f702'),
        'wrapper-fold-read':('PointerSequenceReadBounds','0x209beb8'),
        'producer-null-output':('Invalid memory write (UC_ERR_WRITE_UNMAPPED)','0x209bc0e')}
    assert not any(v['actualReturn'] or v['postFaultStateClaim'] for v in oracle['unsupported'])
    rows,entries,cache=[],{},{}
    for raw in oracle['matches']:
        row=dict(raw)
        row.update(row['realLinkSnapshot'])
        at=int(row['address'],0)
        assert at==0x0209BBFC and row['mode']=='thumb' and row['compiledBytes']==60 and row['exactByteEqual']
        assert dependencies_current(row)
        for p,h in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT/row[p]).read_bytes())==row[h]
        own=native_entry('main',at,cache)
        assert row['nativeAlias']==own['nativeAlias'] and row['bytes']==own['bytes']==60
        metadata,binary,functions=cache['main']
        off=at-int(metadata['base'],0)
        native=binary[off:off+60]
        linked=(ROOT/row['isolatedCallerBinary']).read_bytes()
        validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert native==linked and len(linked)==60 and validation['exactCallerBytes'] is True
        assert validation['linkerAttempt']['exitCode']==0 and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256']
        assert validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        row.update(outputSha256=sha(linked),linked=False,exactBytes=60,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            signature='s32 '+row['name']+'(const u8 **output)',oracle=dict(supported=True,cases=1412,actualReturns=2824,
                report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        rows.append(row)
        entries[row['name']]=own
        for rel in row['relocations']:
            target=int(rel['target'],0)
            entries[rel['symbol']]=data_entry('main',target,cache) if rel['targetMode']=='data' else native_entry('main',target,cache)
    assert len(rows)==1
    for dep in oracle['runtimeDependencies']:assert sha((ROOT/dep['path']).read_bytes())==dep['sha256']
    deps=[d['path'] for d in oracle['runtimeDependencies']]+[oracle['vectorSidecar']['path'],oracle['wrapperSidecar']['path'],controls['vectorSidecar']['path']]
    deps += [FIXTURE,CONTROL_SCRIPT,CONTROLS,'match_mechanics_save_20261031_lane_pointer_producer.py',
        'match_mechanics_save_20261031_lane_pointer_sequence.py','source_dependencies.py',
        'evidence/application/save_core_pointer_sequence_fixtures_20261031.py','evidence/application/save_core_pointer_sequence_build_20261031.py',
        'evidence/application/save_core_controller_controls_20261031_v2.py',
        'match_mechanics_save_20261029_record33.py','match_mechanics_save_20261029_item_use.py','provenance/seed-manifest.json',
        'evidence/attempts/pointer-producer-boundary-scope-20261031.json']
    deps += [r['source'] for r in rows+controls['builds']]+[v[0]['symbolsFile'] for v in cache.values()]
    counts=dict(oracle['counts'])
    counts.pop('unsupportedLogicalStops')
    counts.update(unsupportedBoundaryStops=len(oracle['unsupported']),logicalGuardStops=sum(v['failureClass']=='AssertionError' for v in oracle['unsupported']),
        unmappedMachineStops=sum(v['failureClass']=='UcError' for v in oracle['unsupported']))
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=rows,
        matchedFunctions=1,matchedBytes=60,sourceCreditAdded=0,registrationPerformedByThisScript=False,
        integratorReviewRequiredForSourceAccessQualifier=True,sourceAccessQualifier=oracle['sourceAccessQualifier'],
        nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(set(deps))],replayRequires=[],
        oracle=dict(cases=1412,actualReturns=2824,actualWrapperReturns=1952,counts=counts,providerKinds=0,providedCalls=0,
            nativeCaseDigest=CASE_DIGEST,reports=[r['oracle'] for r in rows],reproductionCommands=commands),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts']),
        boundaryAddendum=dict(path='docs/2026-10-31-pointer-producer-boundary-addendum.md',sha256=sha((ROOT/'docs/2026-10-31-pointer-producer-boundary-addendum.md').read_bytes())),
        wholeLinkedRebuild=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-pointer-producer.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(functions=1,bytes=60,actualReturns=2824,wrapperReturns=1952,registered=False,reportSha256=sha(target.read_bytes()))))


if __name__=='__main__':main()
