import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_pointer_sequence import native_entry,unpack
from source_dependencies import dependencies_current
import save_core_menu_setup_fixtures_20261031 as P
import save_core_menu_setup_controls_20261031 as C
SOURCE_SHA='f830db58dcf68345d2b2e41d8bf0a4388ad07d8970c142d5986fc4a10d60cb5e'
FIXTURE='evidence/application/save_core_menu_setup_fixtures_20261031.py'
ORACLE='evidence/application/save-core-menu-setup-source-20261031.json'
CONTROL_SCRIPT='evidence/application/save_core_menu_setup_controls_20261031.py'
CONTROLS='evidence/application/save-core-menu-setup-controls-20261031.json'
CASE='6605452b10ac28271d4dd2d6a006e9bcf08c3bb0ddd592228e191b5c4c6ec0ef'
CONTROL_CASE='72a271ab21b296563f48bd34b21e67de925b84d9e5c3b331a1913ac059ddeb9a'
PREFIX_CASE='78df1190c2271306dcdaad44227d9cfadee838eaecdfe0d95c5cbe4ca9ffb89d'


def runtime_files():
    paths=set()
    for module in list(sys.modules.values()):
        path=getattr(module,'__file__',None)
        if not path:continue
        path=Path(path).resolve()
        if path.is_relative_to(ROOT) and not path.is_relative_to(ROOT/'deps') and path.suffix=='.py':paths.add(path.relative_to(ROOT).as_posix())
    return paths


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4'
    verify_inputs()
    assert sha((ROOT/P.SOURCE).read_bytes())==SOURCE_SHA
    for producer in (FIXTURE,CONTROL_SCRIPT):
        process=subprocess.run([sys.executable,str(ROOT/producer)],capture_output=True,text=True,timeout=300)
        assert process.returncode==0,process.stdout+process.stderr
    oracle=json.loads((ROOT/ORACLE).read_text());controls=json.loads((ROOT/CONTROLS).read_text())
    vectors=unpack(oracle['vectorSidecar'],CASE)
    negatives=unpack(controls['vectorSidecar'],CONTROL_CASE)
    prefixes=unpack(controls['prefixVectorSidecar'],PREFIX_CASE)
    assert len(vectors)==576 and all(v['actualReturn'] for v in vectors)
    assert set.union(*(set(v['ownInstructionOffsets']) for v in vectors))==set(range(0,672,4))
    assert oracle['counts']['actualTopReturns']==1152 and oracle['counts']['providerKinds']==7
    assert len(negatives)==72 and sum(v['independentRejection'] for v in negatives)==51
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in negatives)
    assert len(prefixes)==522 and all(v['actualBoundary'] and not v['actualWholeFunctionReturn'] for v in prefixes)
    row=dict(oracle['matches'][0]);row.update(row['realLinkSnapshot'])
    assert row['bytes']==row['compiledBytes']==672 and row['exactByteEqual'] and row['sourceSha256']==SOURCE_SHA
    assert dependencies_current(row)
    for path,digest in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),
            ('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:assert sha((ROOT/row[path]).read_bytes())==row[digest]
    validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
    assert validation['exactCallerBytes'] and validation['sourceSha256']==SOURCE_SHA and validation['sourceObjectSha256']==row['objectSha256']
    assert validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74' and validation['linkerAttempt']['exitCode']==0
    cache={};own=native_entry('main',0x0206ED18,cache)
    metadata,binary,config=cache['main'];off=0x0206ED18-int(metadata['base'],0)
    native=binary[off:off+672];linked=(ROOT/row['isolatedCallerBinary']).read_bytes()
    assert linked==native and validation['linkedCallerSha256']==sha(native) and validation['nativeSpanSha256']==sha(native)
    row.update(outputSha256=sha(linked),linked=False,exactBytes=672,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
        signature='u32 native_main_0206ed18(void)',oracle=dict(supported=True,cases=576,actualReturns=1152,report=ORACLE,
            reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
    entries={row['name']:own}
    for rel in row['relocations']:entries[rel['symbol']]=native_entry('main',int(rel['target'],0),cache)
    deps=runtime_files()|{P.SOURCE,ORACLE,CONTROLS,FIXTURE,CONTROL_SCRIPT,oracle['vectorSidecar']['path'],controls['vectorSidecar']['path'],
        controls['prefixVectorSidecar']['path'],'provenance/seed-manifest.json','match_mechanics_save_20261031_lane_menu_setup.py'}
    deps.update(r['source'] for r in controls['builds'])
    deps.update(v[0]['symbolsFile'] for v in cache.values())
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=[row],matchedFunctions=1,matchedBytes=672,
        nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],
        oracle=dict(cases=576,actualReturns=1152,counts=oracle['counts'],nativeCaseDigest=CASE,report=ORACLE),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts'],nativeCaseDigest=CONTROL_CASE),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-menu-setup.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(dict(functions=1,bytes=672,actualReturns=1152,negativeReturns=144,reportSha256=sha(target.read_bytes())))


if __name__=='__main__':main()
