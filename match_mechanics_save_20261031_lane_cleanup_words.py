import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
import save_core_cleanup_words_fixtures_20261031 as P
import save_core_cleanup_words_controls_20261031 as C
ORACLE='evidence/application/save-core-cleanup-words-source-20261031.json'
CONTROLS='evidence/application/save-core-cleanup-words-controls-20261031.json'
PROFILE='evidence/lanes/save-core/cleanup-words-profile-20261031.json'
CASE='a427404a910e7ea31d6388fe1f97306f7894a3f302aa9d325a15fa8651144000'
CONTROL_CASE='f6cce1f923889a6282e05e808aeb4c3520022b8d99735364f9c8c5ad007adb3d'
SOURCES={33975568: 'edc23438a760d5a938a4164723c9a95004f61f7215a88de942d5029bd8fd8bd1', 33976032: 'c1146b769e0075675bb8b522286f9ab73ea6e937428aa328f02f16e99fad12cf', 33938372: '4f1d98a29bac0e7a8cc64b59c7c2ba94e12424a0d14ddf4496837298c2e10494'}
PROFILE_SHA='8d8c53def244e2d13d9acf46bf6cd2ee0b2c3077b5e7285267998fbd30af8504'


HEADER='src/mechanics_save/20261031_lane_cleanup_words/cleanup_words.h'
HEADER_SHA='40af1c049df6a381e278fa819f27ffdd40a0bcb0203230ebe749338a29ac4b82'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs();assert sha((ROOT/PROFILE).read_bytes())==PROFILE_SHA
    assert sha((ROOT/HEADER).read_bytes())==HEADER_SHA
    producers=['evidence/application/save_core_cleanup_words_fixtures_20261031.py','evidence/application/save_core_cleanup_words_controls_20261031.py']
    for producer in producers:
        process=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text())
    vectors=unpack(oracle['vectorSidecar'],CASE);negatives=unpack(controls['vectorSidecar'],CONTROL_CASE)
    assert len(vectors)==916 and all(v['actualReturn'] for v in vectors)
    assert oracle['counts']['actualTopReturns']==1832 and oracle['counts']['providerAddresses']==1 and oracle['counts']['actualNativeHelperReturns']==2096
    assert len(oracle['unsupported'])==2 and not any(v['actualReturn'] for v in oracle['unsupported'])
    assert len(negatives)==1832 and sum(v['independentRejection'] for v in negatives)==1268
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in negatives)
    cache={};entries={};rows=[]
    for raw in oracle['matches']:
        row=dict(raw);row.update(row['realLinkSnapshot']);address=int(row['address'],0);spec=P.M.SPECS[address];length=spec['bytes']
        assert row['sourceSha256']==SOURCES[address] and row['compiledBytes']==row['bytes']==length and row['exactByteEqual'] and row['mode']=='arm'
        assert dependencies_current(row)
        for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),
                ('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
        own=native_entry('main',address,cache);metadata,binary,config=cache['main'];offset=address-int(metadata['base'],0)
        native=binary[offset:offset+length];linked=(ROOT/row['isolatedCallerBinary']).read_bytes();validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert linked==native and validation['exactCallerBytes'] and validation['sourceSha256']==SOURCES[address]
        assert validation['sourceObjectSha256']==row['objectSha256'] and validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        assert validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
        own_vectors=[v for v in vectors if v['profile']['entry']==address]
        expected=set(range(0,spec['code'],4))
        assert set.union(*(set(v['ownInstructionOffsets']) for v in own_vectors))==expected
        row.update(outputSha256=sha(linked),linked=False,exactBytes=length,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            oracle=dict(supported=True,cases=len(own_vectors),actualReturns=2*len(own_vectors),report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        rows.append(row);entries[row['name']]=own
        for rel in row['relocations']:entries[rel['symbol']]=(data_entry if rel['kind']=='data' else native_entry)('main',int(rel['target'],0),cache)
    deps=runtime_files()|set(producers)|{ORACLE,CONTROLS,PROFILE,HEADER,oracle['vectorSidecar']['path'],controls['vectorSidecar']['path'],
        'provenance/seed-manifest.json','match_mechanics_save_20261031_lane_cleanup_words.py'}
    deps.update(r['source'] for r in rows+controls['builds']);deps.update(v[0]['symbolsFile'] for v in cache.values())
    for r in rows+controls['builds']:deps.update(d['path'] for d in r.get('sourceDependencies',[]))
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=rows,matchedFunctions=3,matchedBytes=156,
        nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],
        oracle=dict(cases=len(vectors),actualReturns=2*len(vectors),counts=oracle['counts'],nativeCaseDigest=CASE,report=ORACLE),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts'],nativeCaseDigest=CONTROL_CASE),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-cleanup-words.json';target.write_text(json.dumps(report,indent=2)+'\n')
    print(dict(functions=3,bytes=156,actualReturns=1832,negativeReturns=3664,reportSha256=sha(target.read_bytes())))


if __name__=='__main__':main()
