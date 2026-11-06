import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_input_state_family_fixtures_20261031 as P
import save_core_input_state_family_controls_20261031 as C
ORACLE='evidence/application/save-core-input-state-family-source-20261031.json'
CONTROLS='evidence/application/save-core-input-state-family-controls-20261031.json'
PROFILE='evidence/lanes/save-core/input-state-family-profile-20261031.json'
CASE='01b2ac6e9fb0e397da30d1efacc9847f73966ddb6e4738e7899df186602c842f'
CONTROL_CASE='e53c11dad1e5397292bd1b2c0cda00c7787d5849325e39e0ffd276423dff8c7b'
PROFILE_SHA='32dba10ae3ead29c31ee903b001688a334502d953722eae8ecc154b8121cdba3'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4';verify_inputs();assert sha((ROOT/PROFILE).read_bytes())==PROFILE_SHA
    producers=['evidence/application/save_core_input_state_family_fixtures_20261031.py','evidence/application/save_core_input_state_family_controls_20261031.py']
    for producer in producers:
        process=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=300);assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text());vectors=unpack(oracle['vectorSidecar'],CASE);negatives=unpack(controls['vectorSidecar'],CONTROL_CASE)
    assert len(vectors)==4346 and all(v['actualReturn'] for v in vectors) and oracle['counts']['actualTopReturns']==8692 and oracle['counts']['physicalNativeReturnInstructions']==15772 and oracle['counts']['providerCalls']==144
    assert len(negatives)==6138 and sum(v['independentRejection'] for v in negatives)==2930 and all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in negatives)
    profiles=json.loads((ROOT/PROFILE).read_text())['rows'];cache={};matches=[];entries={}
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot']);address=int(row['address'],0);p=next(p for p in profiles if int(p['address'],0)==address);length=p['bytes'];assert row['sourceSha256']==p['sourceSha256'] and row['compiledBytes']==row['bytes']==length and row['exactByteEqual'] and dependencies_current(row)
        for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
        own=native_entry('main',address,cache);metadata,binary,config=cache['main'];offset=address-int(metadata['base'],0);native=binary[offset:offset+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text());assert native==linked and validation['exactCallerBytes'] and validation['sourceSha256']==row['sourceSha256']
        assert validation['sourceObjectSha256']==row['objectSha256'] and validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked) and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
        selected=[v for v in vectors if v['entry']==address];code=P.M.FUNCTIONS[address][1];decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB);expected={i.address-address for i in decoder.disasm(native[:code],address)};assert set.union(*(set(v['ownInstructionOffsets']) for v in selected))==expected
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,oracle=dict(supported=True,cases=len(selected),actualReturns=2*len(selected),report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        row['returnContract']=dict(sourceReturnType=('void' if address in (0x02094790,0x0208A5AC) else 'u32'),physicalR0Compared=True,apiReturnProven=False,callerConsumptionComplete=False)
        entries[row['name']]=own
        for rel in row['relocations']:entries[rel['symbol']]=(data_entry if rel['kind']=='data' else native_entry)('main',int(rel['target'],0),cache)
        matches.append(row)
    assert len(matches)==4 and sum(r['bytes'] for r in matches)==378
    deps=runtime_files()|set(producers)|{ORACLE,CONTROLS,PROFILE,oracle['vectorSidecar']['path'],controls['vectorSidecar']['path'],'provenance/seed-manifest.json','match_mechanics_save_20261031_lane_input_state_family.py'}
    rows=matches+controls['builds']+oracle['reusedAcceptedBuilds'];deps.update(r['source'] for r in rows)
    for row in rows:deps.update(p['path'] for p in row.get('sourceDependencies',[]))
    deps.update(v[0]['symbolsFile'] for v in cache.values());verify_inputs()
    out=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=matches,matchedFunctions=4,matchedBytes=378,reusedAcceptedBytes=88,reusedNewCredit=0,nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],oracle=dict(cases=4346,actualReturns=8692,nativeCaseDigest=CASE,report=ORACLE,counts=oracle['counts']),negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts'],nativeCaseDigest=CONTROL_CASE),wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-input-state-family.json';target.write_text(json.dumps(out,indent=2)+'\n');print(dict(functions=4,bytes=378,actualReturns=8692,wrongReturns=12276,reportSha256=sha(target.read_bytes())))


if __name__=='__main__':main()
