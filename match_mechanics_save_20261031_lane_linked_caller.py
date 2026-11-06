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
import save_core_linked_caller_fixtures_20261031 as P
import save_core_linked_caller_controls_20261031 as C
ORACLE='evidence/application/save-core-linked-caller-source-20261031.json'
CONTROLS='evidence/application/save-core-linked-caller-controls-20261031.json'
PROFILE='evidence/lanes/save-core/linked-caller-profile-20261031.json'
CASE='fbc7ab9ebf61d13db8168f9e0495145fe44af539075abd35d92cb6f2d6194413'
CONTROL_CASE='720b879fa98d593ce9fd5f3f697474c87fadba7f029f626a1d181306a85dd41b'
PROFILE_SHA='7da0366bab46853c0092b935811af6a55a6c8c3698e29df4c7f5b78183aabd82'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4';verify_inputs();assert sha((ROOT/PROFILE).read_bytes())==PROFILE_SHA
    producers=['evidence/application/save_core_linked_caller_fixtures_20261031.py','evidence/application/save_core_linked_caller_controls_20261031.py']
    for producer in producers:
        process=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=300);assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text());vectors=unpack(oracle['vectorSidecar'],CASE);negatives=unpack(controls['vectorSidecar'],CONTROL_CASE)
    assert len(vectors)==905 and all(v['actualReturn'] for v in vectors) and oracle['counts']['actualTopReturns']==1810 and oracle['counts']['physicalActualHelperReturns']==7202 and oracle['counts']['suppliedLowerCalls']==9830 and oracle['counts']['syntheticStackPerturbations']==96
    assert len(oracle['unsupported'])==2 and all(not v['actualReturn'] and v['returnCredit']==0 for v in oracle['unsupported'])
    assert len(negatives)==3620 and sum(v['independentRejection'] for v in negatives)==806 and all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in negatives)
    profiles=json.loads((ROOT/PROFILE).read_text())['rows'];cache={};matches=[];entries={}
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot']);address=int(row['address'],0);p=next(p for p in profiles if int(p['address'],0)==address);length=p['bytes'];assert row['sourceSha256']==p['sourceSha256'] and row['compiledBytes']==row['bytes']==length and row['exactByteEqual'] and dependencies_current(row)
        for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
        own=native_entry('main',address,cache);metadata,binary,config=cache['main'];offset=address-int(metadata['base'],0);native=binary[offset:offset+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text());assert native==linked and validation['exactCallerBytes'] and validation['sourceSha256']==row['sourceSha256']
        assert validation['sourceObjectSha256']==row['objectSha256'] and validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked) and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
        expected={i.address-address for i in Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(native[:242],address)};assert set.union(*(set(v['ownInstructionOffsets']) for v in vectors))==expected
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,oracle=dict(supported=True,cases=905,actualReturns=1810,report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        row['returnContract']=dict(sourceReturnType='u32',physicalR0Compared=True,apiReturnProven=False,callerConsumptionComplete=False);entries[row['name']]=own
        for rel in row['relocations']:entries[rel['symbol']]=(data_entry if rel['kind']=='data' else native_entry)('main',int(rel['target'],0),cache)
        matches.append(row)
    assert len(matches)==1 and sum(r['bytes'] for r in matches)==252
    deps=runtime_files()|set(producers)|{ORACLE,CONTROLS,PROFILE,oracle['vectorSidecar']['path'],controls['vectorSidecar']['path'],'provenance/seed-manifest.json','match_mechanics_save_20261031_lane_linked_caller.py'}
    rows=matches+controls['builds']+oracle['reusedAcceptedBuilds'];deps.update(r['source'] for r in rows)
    for row in rows:deps.update(p['path'] for p in row.get('sourceDependencies',[]))
    for address in tuple(P.M.FUNCTIONS)+tuple(P.M.PROVIDERS):entries[f'qualified_native_{address:08x}']=native_entry('main',address,cache)
    deps.update(v[0]['symbolsFile'] for v in cache.values());deps.update(origin for address,origin,source_hash in P.REUSE);verify_inputs()
    out=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=matches,matchedFunctions=1,matchedBytes=252,reusedAcceptedBytes=220,reusedNewCredit=0,nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={},sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],oracle=dict(cases=905,actualReturns=1810,nativeCaseDigest=CASE,report=ORACLE,counts=oracle['counts']),negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts'],nativeCaseDigest=CONTROL_CASE),wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-linked-caller.json';target.write_text(json.dumps(out,indent=2)+'\n');print(dict(functions=1,bytes=252,actualReturns=1810,wrongReturns=7240,reportSha256=sha(target.read_bytes())))


if __name__=='__main__':main()
