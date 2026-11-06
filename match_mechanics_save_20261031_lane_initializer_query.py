import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_initializer_query_fixtures_20261031 as P
import save_core_initializer_query_controls_20261031 as C
ORACLE='evidence/application/save-core-initializer-query-source-20261031.json'
CONTROLS='evidence/application/save-core-initializer-query-controls-20261031.json'
PROFILE='evidence/lanes/save-core/initializer-query-profile-20261031.json'
CASE='e58504b57d1f1a769205cd3a50ac732a369330d7994db657496aab1cb5a13483'
CONTROL_CASE='9a6294babacea2f74a73a915c672f6da25df516db3ae705693cf77613e5d1aee'
SOURCES={34094900: '15d92dc74495fe08564f21f20080749f6b9a419da08c32bb9e1cdc4c5d07537e', 34149708: 'b10b8dce719a78bca5055b5121d1b7ae12af861787710fc799efc70d0b288239', 34315528: 'e73e3d21056597ac4175a63bbb361d67edf7361974673f108b959e01de8dd2ab'}
PROFILE_SHA='e56613a3174a99790f43e9547f48bcc084610df2d725024c231c55b57e0e87f0'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs();assert sha((ROOT/PROFILE).read_bytes())==PROFILE_SHA
    producers=['evidence/application/save_core_initializer_query_fixtures_20261031.py','evidence/application/save_core_initializer_query_controls_20261031.py']
    for producer in producers:
        process=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text())
    vectors=unpack(oracle['vectorSidecar'],CASE);negatives=unpack(controls['vectorSidecar'],CONTROL_CASE)
    assert len(vectors)==770 and all(v['actualReturn'] for v in vectors)
    assert oracle['counts']['actualTopReturns']==1540 and oracle['counts']['providers']==0 and oracle['counts']['actualNativeHelperReturns']==1246
    assert len(oracle['unsupported'])==4 and not any(v['actualReturn'] for v in oracle['unsupported'])
    assert len(negatives)==1102 and sum(v['independentRejection'] for v in negatives)==225
    assert all(v['native']['actualReturn'] and v['compiledVariant']['actualReturn'] for v in negatives)
    cache={};entries={};rows=[]
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot']);address=int(row['address'],0);spec=P.M.SPECS[address];length=spec['bytes']
        assert row['sourceSha256']==SOURCES[address] and row['compiledBytes']==row['bytes']==length and row['exactByteEqual'] and row['mode']==spec['mode']
        assert dependencies_current(row)
        for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),
                ('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
        own=native_entry('main',address,cache);metadata,binary,config=cache['main'];offset=address-int(metadata['base'],0)
        native=binary[offset:offset+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert linked==native and validation['exactCallerBytes'] and validation['sourceSha256']==SOURCES[address]
        assert validation['sourceObjectSha256']==row['objectSha256'] and validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        assert validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
        own_vectors=[v for v in vectors if v['profile']['entry']==address]
        decoder=P.Cs(P.CS_ARCH_ARM,P.CS_MODE_THUMB if spec['mode']=='thumb' else P.CS_MODE_ARM)
        expected={i.address-address for i in decoder.disasm(native[:spec['code']],address)}
        assert set.union(*(set(v['ownInstructionOffsets']) for v in own_vectors))==expected
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            oracle=dict(supported=True,cases=len(own_vectors),actualReturns=2*len(own_vectors),report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        rows.append(row);entries[row['name']]=own
        for rel in row['relocations']:entries[rel['symbol']]=(data_entry if rel['kind']=='data' else native_entry)('main',int(rel['target'],0),cache)
    deps=runtime_files()|set(producers)|{ORACLE,CONTROLS,PROFILE,oracle['vectorSidecar']['path'],controls['vectorSidecar']['path'],
        'provenance/seed-manifest.json','match_mechanics_save_20261031_lane_initializer_query.py'}
    deps.update(r['source'] for r in rows+controls['builds']);deps.update(v[0]['symbolsFile'] for v in cache.values())
    for r in rows+controls['builds']:deps.update(d['path'] for d in r.get('sourceDependencies',[]))
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=rows,matchedFunctions=3,matchedBytes=208,
        nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],
        oracle=dict(cases=len(vectors),actualReturns=2*len(vectors),counts=oracle['counts'],nativeCaseDigest=CASE,report=ORACLE),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts'],nativeCaseDigest=CONTROL_CASE),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-initializer-query.json';target.write_text(json.dumps(report,indent=2)+'\n')
    print(dict(functions=3,bytes=208,actualReturns=1540,negativeReturns=2204,reportSha256=sha(target.read_bytes())))


if __name__=='__main__':main()
