import collections,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_byte_sequence_fixtures_20261101 as P
import save_core_byte_sequence_controls_20261101 as C
ORACLE='evidence/application/save-core-byte-sequence105-source-20261101.json'
CONTROLS='evidence/application/save-core-byte-sequence105-controls-20261101.json'
PROFILE='evidence/lanes/save-core/byte-sequence105-profile-20261101.json'
CASE='84c85e1d547a574098123b2f69efa71ec40ae4764dfb455efb8ae6809bf7cd16'
CONTROL_CASE='34d4ee7fe6511cf6fa03e9004da1ddd17e9ef2546903cd9077ef0614dde29b0c'
PROFILE_SHA='654151f6db486d4f1f9bc0bebc73322553a6f046bd8edea4024ab1b70fce2d95'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4';verify_inputs();assert sha((ROOT/PROFILE).read_bytes())==PROFILE_SHA
    producers=['evidence/application/save_core_byte_sequence_fixtures_20261101.py','evidence/application/save_core_byte_sequence_controls_20261101.py']
    for producer in producers:
        process=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=420);assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text());vectors=unpack(oracle['vectorSidecar'],CASE);negatives=unpack(controls['vectorSidecar'],CONTROL_CASE);profiles=json.loads((ROOT/PROFILE).read_text())['rows'];assert len(vectors)==4760 and all(v['actualReturn'] and v['backingUnchanged'] and not v['nonStackWrites'] for v in vectors);assert oracle['counts']['actualTopReturns']==14280 and oracle['counts']['observedNativeHelperReturns']==251940 and not oracle['counts']['suppliedFunctions'];assert len(negatives)==644 and all(v['actualOriginalReturn'] and v['actualPositiveReturn'] and v['actualWrongReturn'] for v in negatives) and sum(v['independentReturnRejected'] for v in negatives)==95
    helper_returns=collections.Counter(v['entry'] for case in vectors for v in case['physicalNativeReturns']);cache={};entries={};matches=[]
    for raw in [*oracle['matches'],*oracle['reusedMatches']]:
        row=dict(raw);row.update(row['realLinkSnapshot']);address=int(row['address'],0);length=row['bytes'];assert row['compiledBytes']==length and row['exactByteEqual'] and dependencies_current(row)
        for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
        own=native_entry('main',address,cache);metadata,binary,config=cache['main'];offset=address-int(metadata['base'],0);native=binary[offset:offset+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text());assert native==linked and validation['exactCallerBytes'] and validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256'] and validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked) and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
        entries[row['name']]=own
        for rel in row['relocations']:entries[rel['symbol']]=(data_entry if rel['kind']=='data' else native_entry)('main',int(rel['target'],0),cache)
        if address not in (0x207AFEC,0x207B674):
            p=next(p for p in profiles if int(p['address'],0)==address);assert row['sourceSha256']==p['sourceSha256'];actual=14280 if address==P.M.ENTRY else helper_returns[address]*3
            row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,newCoverage=p['newCoverage'],oracle=dict(supported=True,actualReturns=actual,ownEntryCases=4760 if address==P.M.ENTRY else sum(any(v['entry']==address for v in case['physicalNativeReturns']) for case in vectors),compiledAlternativeActualReturns=9520 if address==P.M.ENTRY else helper_returns[address],report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
            if not p['newCoverage']:assert sha((ROOT/p['oldSource']).read_bytes())==p['oldSourceSha256'];row.update(zeroCoverageMigration=True,oldSource=p['oldSource'],oldSourceSha256=p['oldSourceSha256'])
            matches.append(row)
    assert len(matches)==5 and sum(r['bytes'] for r in matches)==860 and sum(r['bytes'] for r in matches if r['newCoverage'])==440;assert set.union(*(set(v['ownInstructionOffsets']) for v in vectors))==set(range(0,440,4))
    deps=runtime_files()|set(producers)|{ORACLE,CONTROLS,PROFILE,oracle['vectorSidecar']['path'],controls['vectorSidecar']['path'],'provenance/seed-manifest.json','match_mechanics_save_20261101_lane_byte_sequence.py'};allrows=[*oracle['matches'],*oracle['reusedMatches'],*[r['match'] for r in controls['controls']]];deps.update(r['source'] for r in allrows);deps.update(p['oldSource'] for p in profiles if not p['newCoverage'])
    for row in allrows:deps.update(p['path'] for p in row.get('sourceDependencies',[]))
    for address in [P.M.ENTRY,*P.M.HELPERS]:entries[f'qualified_native_{address:08x}']=native_entry('main',address,cache)
    deps.update(v[0]['symbolsFile'] for v in cache.values());verify_inputs();out=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=matches,matchedFunctions=5,matchedBytes=860,netNewCandidateFunctions=1,netNewCandidateBytes=440,zeroCoverageAlternativeFunctions=4,zeroCoverageAlternativeBytes=420,reusedAcceptedBytes=80,reusedNewCredit=0,nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={},sourceDependencies=[],replayDependencies=[file_identity(Path(p).as_posix()) for p in sorted(deps)],replayRequires=[],oracle=dict(cases=4760,actualReturns=14280,nativeCaseDigest=CASE,report=ORACLE,counts=oracle['counts']),negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts'],nativeCaseDigest=CONTROL_CASE),wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations']);target=ROOT/'evidence/matches/mechanics-save-20261101-lane-byte-sequence.json';target.write_text(json.dumps(out,indent=2)+'\n');print(dict(newFunctions=1,newBytes=440,migrations=4,zeroBytes=420,actualReturns=14280,wrongReturns=644,reportSha256=sha(target.read_bytes())))


if __name__=='__main__':main()
