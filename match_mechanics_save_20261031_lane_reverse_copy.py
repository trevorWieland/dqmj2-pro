import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_reverse_copy_fixtures_20261031 as P
import save_core_reverse_copy_controls_20261031 as C
ORACLE='evidence/application/save-core-reverse-copy-source-20261031.json'
CONTROLS='evidence/application/save-core-reverse-copy-controls-20261031.json'
PROFILE='evidence/lanes/save-core/reverse-copy-profile-20261031.json'
CASE='dabab5f9ba68381b683eb67e03519125833da9cb01922f441aeeda447d563b09'
CONTROL_CASE='f0a4c526918b490512a5f90652dafdff6c089d788fb3e552e24131e9c3ae8b95'
SOURCE_SHA='1a7bfa1bcc6196fdd4166319c4832f55536cc1c5245f5af8cc8631bb84704d42'
PROFILE_SHA='80b2e74c9d47549c8ecd915169928964f582f51a7b7380ac909b5d4706911733'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs();assert sha((ROOT/PROFILE).read_bytes())==PROFILE_SHA
    producers=['evidence/application/save_core_reverse_copy_fixtures_20261031.py','evidence/application/save_core_reverse_copy_controls_20261031.py']
    for producer in producers:
        process=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text())
    vectors=unpack(oracle['vectorSidecar'],CASE);negatives=unpack(controls['vectorSidecar'],CONTROL_CASE)
    assert len(vectors)==714 and all(v['actualReturn'] for v in vectors)
    assert oracle['counts']['actualTopReturns']==1428 and oracle['counts']['providers']==0
    assert len(oracle['unsupported'])==6 and not any(v['actualReturn'] for v in oracle['unsupported'])
    assert len(negatives)==1428 and sum(v['independentRejection'] for v in negatives)==837
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in negatives)
    row=dict(oracle['matches'][0]);row.update(row['realLinkSnapshot']);address=int(row['address'],0);length=44
    assert address==0x02094240 and row['sourceSha256']==SOURCE_SHA and row['compiledBytes']==row['bytes']==length and row['exactByteEqual']
    assert dependencies_current(row)
    for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),
            ('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
    cache={};own=native_entry('main',address,cache);metadata,binary,config=cache['main'];offset=address-int(metadata['base'],0)
    native=binary[offset:offset+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
    assert linked==native and validation['exactCallerBytes'] and validation['sourceSha256']==SOURCE_SHA
    assert validation['sourceObjectSha256']==row['objectSha256'] and validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
    assert validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
    assert set.union(*(set(v['ownInstructionOffsets']) for v in vectors))==set(range(0,length,2))
    row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
        oracle=dict(supported=True,cases=len(vectors),actualReturns=2*len(vectors),report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
    entries={row['name']:own}
    for rel in row['relocations']:entries[rel['symbol']]=native_entry('main',int(rel['target'],0),cache)
    deps=runtime_files()|set(producers)|{ORACLE,CONTROLS,PROFILE,oracle['vectorSidecar']['path'],controls['vectorSidecar']['path'],
        'provenance/seed-manifest.json','match_mechanics_save_20261031_lane_reverse_copy.py'}
    deps.update(r['source'] for r in [row]+controls['builds']);deps.update(v[0]['symbolsFile'] for v in cache.values())
    for r in [row]+controls['builds']:deps.update(d['path'] for d in r.get('sourceDependencies',[]))
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=[row],matchedFunctions=1,matchedBytes=length,
        nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],
        oracle=dict(cases=len(vectors),actualReturns=2*len(vectors),counts=oracle['counts'],nativeCaseDigest=CASE,report=ORACLE),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts'],nativeCaseDigest=CONTROL_CASE),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-reverse-copy.json';target.write_text(json.dumps(report,indent=2)+'\n')
    print(dict(functions=1,bytes=length,actualReturns=1428,negativeReturns=2856,reportSha256=sha(target.read_bytes())))


if __name__=='__main__':main()
