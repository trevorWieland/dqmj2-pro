import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_group_criterion_fixtures_20261031 as P
import save_core_group_criterion_controls_20261031 as C
ORACLE='evidence/application/save-core-group-criterion-source-20261031.json'
CONTROLS='evidence/application/save-core-group-criterion-controls-20261031.json'
CASE='7d956303b9141a9c3209f298dc500237fa5f1610592714dc769598adaf689ad7'
CONTROL_CASE='ef501f5ebc0f8dbeede2ce1f3f1dde89bfd568fa83d74b9e8d93ea5466c322f7'
SOURCES={0x020645B0:'665afd3144f006d4a03871ec4c641ec1a9581a8d47271ceee25a4b807d373a49',
    0x02064654:'8118d876b14ba23f6286d0730f60bb3198ad2e1feb8a7a41ec20e4e1dcbad288'}
HEADER='src/mechanics_save/20261031_lane_group_criterion/group_criterion.h'
HEADER_SHA='58c069acde83787a3854f855a3e474ecb0599549afb28135b0bcd7c9512e31ed'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs();assert sha((ROOT/HEADER).read_bytes())==HEADER_SHA
    producers=['evidence/application/save_core_group_criterion_fixtures_20261031.py','evidence/application/save_core_group_criterion_controls_20261031.py']
    for producer in producers:
        process=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text())
    vectors=unpack(oracle['vectorSidecar'],CASE);negatives=unpack(controls['vectorSidecar'],CONTROL_CASE)
    assert len(vectors)==15050 and all(v['actualReturn'] and v['dataWrites']==0 for v in vectors)
    assert oracle['counts']['actualTopReturns']==30100 and oracle['counts']['providers']==0 and oracle['counts']['actualNativeHelperReturns']==69636
    assert len(oracle['unsupported'])==3 and not any(v['actualReturn'] for v in oracle['unsupported'])
    assert len(negatives)==155 and sum(v['independentRejection'] for v in negatives)==16
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in negatives)
    cache={};entries={};rows=[]
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot']);address=int(row['address'],0);length=P.SPECS[address]
        assert row['sourceSha256']==SOURCES[address] and row['compiledBytes']==row['bytes']==length and row['exactByteEqual']
        assert dependencies_current(row)
        for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),
                ('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
        own=native_entry('main',address,cache);metadata,binary,config=cache['main'];offset=address-int(metadata['base'],0)
        native=binary[offset:offset+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes()
        validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert linked==native and validation['exactCallerBytes'] and validation['sourceSha256']==SOURCES[address]
        assert validation['sourceObjectSha256']==row['objectSha256'] and validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        assert validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
        own_vectors=[v for v in vectors if v['profile']['entry']==address]
        assert set.union(*(set(v['ownInstructionOffsets']) for v in own_vectors))==set(range(0,length,4))
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            oracle=dict(supported=True,cases=len(own_vectors),actualReturns=2*len(own_vectors),report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        rows.append(row);entries[row['name']]=own
        for rel in row['relocations']:entries[rel['symbol']]=native_entry('main',int(rel['target'],0),cache)
    deps=runtime_files()|set(producers)|{ORACLE,CONTROLS,HEADER,oracle['vectorSidecar']['path'],controls['vectorSidecar']['path'],
        'provenance/seed-manifest.json','match_mechanics_save_20261031_lane_group_criterion.py'}
    deps.update(r['source'] for r in rows+controls['builds']);deps.update(v[0]['symbolsFile'] for v in cache.values())
    for r in rows+controls['builds']:deps.update(d['path'] for d in r.get('sourceDependencies',[]))
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=rows,matchedFunctions=2,matchedBytes=288,
        nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],
        oracle=dict(cases=15050,actualReturns=30100,counts=oracle['counts'],nativeCaseDigest=CASE,report=ORACLE),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts'],nativeCaseDigest=CONTROL_CASE),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-group-criterion.json';target.write_text(json.dumps(report,indent=2)+'\n')
    print(dict(functions=2,bytes=288,actualReturns=30100,negativeReturns=310,reportSha256=sha(target.read_bytes())))


if __name__=='__main__':main()
