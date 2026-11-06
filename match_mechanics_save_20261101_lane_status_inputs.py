import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_status_inputs_fixtures_20261101 as P
import save_core_status_inputs_controls_20261101 as C
ORACLE='evidence/application/save-core-status-inputs-source-20261101.json'
CONTROLS='evidence/application/save-core-status-inputs-controls-20261101.json'
PROFILE='evidence/lanes/save-core/status-input-profile-20261101.json'
CASE='10e8dd06fabca6de80e5608a10807fb255ac15de8ca7f7570580a6353a0a82ca'
CONTROL_CASE='238ad43e395c8c984fd3aeb6657248cbd0572305288ccb8506d1d731c642dbcd'
PROFILE_SHA='5aaaf161e85f44dbb85b6f7af7ffad074068211ce037ebe3db8776e3f0f0661b'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4';verify_inputs();assert sha((ROOT/PROFILE).read_bytes())==PROFILE_SHA
    producers=['evidence/application/save_core_status_inputs_fixtures_20261101.py','evidence/application/save_core_status_inputs_controls_20261101.py']
    for producer in producers:
        process=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=300);assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text());vectors=unpack(oracle['vectorSidecar'],CASE);negatives=unpack(controls['vectorSidecar'],CONTROL_CASE)
    assert len(vectors)==3964 and all(v['actualReturn'] for v in vectors) and oracle['counts']['actualTopReturns']==7928 and oracle['counts']['physicalActualHelperReturns']==16992 and oracle['counts']['suppliedLowerCalls']==1152 and oracle['counts']['syntheticFieldPerturbations']==24
    assert len(negatives)==433 and sum(v['independentRejection'] for v in negatives)==235 and all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in negatives)
    profiles=json.loads((ROOT/PROFILE).read_text())['rows'];cache={};matches=[];entries={}
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot']);address=int(row['address'],0);p=next(p for p in profiles if int(p['address'],0)==address);length=p['bytes'];assert row['sourceSha256']==p['sourceSha256'] and row['compiledBytes']==row['bytes']==length and row['exactByteEqual'] and dependencies_current(row)
        for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
        own=native_entry('main',address,cache);metadata,binary,config=cache['main'];offset=address-int(metadata['base'],0);native=binary[offset:offset+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text());assert native==linked and validation['exactCallerBytes'] and validation['sourceSha256']==row['sourceSha256']
        assert validation['sourceObjectSha256']==row['objectSha256'] and validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked) and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
        selected=[v for v in vectors if v['entry']==address];assert set.union(*(set(v['ownInstructionOffsets']) for v in selected))==set(range(0,p['codeBytes'],4))
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,oracle=dict(supported=True,cases=len(selected),actualReturns=2*len(selected),report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        row['returnContract']=dict(sourceReturnType='u32',physicalR0Compared=True,apiReturnProven=False,callerConsumptionComplete=False);entries[row['name']]=own
        for rel in row['relocations']:entries[rel['symbol']]=(data_entry if rel['kind']=='data' else native_entry)('main',int(rel['target'],0),cache)
        matches.append(row)
    assert len(matches)==4 and sum(r['bytes'] for r in matches)==344
    deps=runtime_files()|set(producers)|{ORACLE,CONTROLS,PROFILE,oracle['vectorSidecar']['path'],controls['vectorSidecar']['path'],'provenance/seed-manifest.json','match_mechanics_save_20261101_lane_status_inputs.py'}
    rows=matches+controls['builds']+oracle['reusedAcceptedBuilds'];deps.update(r['source'] for r in rows)
    for row in rows:deps.update(p['path'] for p in row.get('sourceDependencies',[]))
    for address in tuple(P.M.OWN)+tuple(P.M.HELPERS)+tuple(P.M.PROVIDERS):entries[f'qualified_native_{address:08x}']=native_entry('main',address,cache)
    deps.update(v[0]['symbolsFile'] for v in cache.values());deps.update(origin for address,origin,source_hash in P.REUSE);verify_inputs()
    interior=[dict(entry='0x02025FA0',parentEntry='0x02025F1C',parentSpanSha256=entries['qualified_native_02025f1c']['nativeSpanSha256'],edge='original260F4 conditional path to26100 then B25FA0;shared division tail,no new function/return entry'),dict(entry='0x02026358',parentEntry='0x02026350',parentSpanSha256=entries['qualified_native_02026350']['nativeSpanSha256'],edge='originalBL at2610C to declared+8 label;physical return independently traced')]
    out=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=matches,matchedFunctions=4,matchedBytes=344,reusedAcceptedBytes=72,reusedNewCredit=0,nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={},observedInteriorCodeEdges=interior,sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],oracle=dict(cases=3964,actualReturns=7928,nativeCaseDigest=CASE,report=ORACLE,counts=oracle['counts']),negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts'],nativeCaseDigest=CONTROL_CASE),wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261101-lane-status-inputs.json';target.write_text(json.dumps(out,indent=2)+'\n');print(dict(functions=4,bytes=344,actualReturns=7928,wrongReturns=866,reportSha256=sha(target.read_bytes())))


if __name__=='__main__':main()
