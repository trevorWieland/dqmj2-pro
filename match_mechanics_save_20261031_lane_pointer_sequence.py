import gzip
import json
from pathlib import Path
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from match_mechanics_save_20261029_record33 import sha,file_identity,verify_inputs,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current
FIXTURE='evidence/application/save_core_pointer_sequence_fixtures_20261031.py'
ORACLE='evidence/application/save-core-pointer-sequence-source-20261031.json'
CONTROL_SCRIPT='evidence/application/save_core_pointer_sequence_controls_20261031.py'
CONTROLS='evidence/lanes/save-core/pointer-sequence-controls-20261031.json'
CASE_DIGEST='2a45452327c3050313479924d1aa74bcff52eb1e2aafc30dade88f124daff4b0'
PRODUCER_DIGEST='50aa0754a0330300dcdb0f853a3382f1aae00a9d967d45a5384b128e3e4c4c69'
CONTROL_DIGEST='e31a055a2ac19ed7764970cba69d737f3c21a43002ea91d390b546346f0b091b'


def native_entry(module,address,cache):
    assert module=='main'
    if module not in cache:
        seed=json.loads((ROOT/'provenance/seed-manifest.json').read_text())
        metadata=next(m for m in seed['modules'] if m['name']==module)
        binary=(ROOT/metadata['binary']).read_bytes()
        assert sha(binary)==metadata['sha256']==MAIN_SHA
        text=(ROOT/metadata['symbolsFile']).read_text()
        functions={int(at,0):(name,mode,int(size,0)) for name,mode,size,at in re.findall(
            r'^(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',text,re.M)}
        cache[module]=metadata,binary,functions
    metadata,binary,functions=cache[module]
    name,mode,length=functions[address]
    off=address-int(metadata['base'],0)
    span=binary[off:off+length]
    assert len(span)==length and mode in ('arm','thumb')
    return dict(address=hex(address),mode=mode,module=module,processor='arm9',kind='function',nativeAlias=name,bytes=length,
        nativeSpanSha256=sha(span),nativeModuleSha256=metadata['sha256'],verification='Declared ARM/Thumb function start and measured complete module/span hashes')


def unpack(sidecar,expected):
    raw=(ROOT/sidecar['path']).read_bytes()
    assert sha(raw)==sidecar['sha256'] and len(raw)==sidecar['compressedBytes']
    decoded=gzip.decompress(raw)
    assert sha(decoded)==sidecar['uncompressedSha256']==expected and len(decoded)==sidecar['uncompressedBytes']
    vectors=json.loads(decoded)
    assert len(vectors)==sidecar['contexts']
    return vectors


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
    assert oracle['counts']['actualEntryReturns']==1952 and oracle['counts']['directProducerReturns']==8
    assert oracle['counts']['actualHelperReturns']==7640 and oracle['counts']['providers']==0
    vectors=unpack(oracle['vectorSidecar'],CASE_DIGEST)
    producer=unpack(oracle['producerControls'],PRODUCER_DIGEST)
    negatives=unpack(controls['vectorSidecar'],CONTROL_DIGEST)
    assert len(vectors)==976 and len(producer)==8 and all(v['actualReturn'] for v in vectors+producer)
    assert len(negatives)==32 and sum(v['independentRejected'] for v in negatives)==8
    assert all(v['native']['actualReturn'] and v['compiledWrongC']['actualReturn'] for v in negatives)
    assert len(oracle['unsupported'])==2 and not any(v['actualReturn'] for v in oracle['unsupported'])
    assert controls['counts']['independentRejections']==8 and controls['counts']['positiveControls']==24
    rows,entries,cache=[],{},{}
    for raw in oracle['matches']:
        row=dict(raw)
        row.update(row['realLinkSnapshot'])
        at=int(row['address'],0)
        assert at==0x0209BC38 and row['mode']=='thumb' and row['compiledBytes']==36 and row['exactByteEqual']
        assert dependencies_current(row)
        for p,h in [('source','sourceSha256'),('object','objectSha256'),('isolatedCallerBinary','isolatedCallerBinarySha256'),('isolatedCallerLinkValidation','isolatedCallerLinkValidationSha256')]:
            assert sha((ROOT/row[p]).read_bytes())==row[h]
        own=native_entry('main',at,cache)
        assert row['nativeAlias']==own['nativeAlias'] and row['bytes']==own['bytes']==36
        metadata,binary,functions=cache['main']
        off=at-int(metadata['base'],0)
        native=binary[off:off+36]
        linked=(ROOT/row['isolatedCallerBinary']).read_bytes()
        validation=json.loads((ROOT/row['isolatedCallerLinkValidation']).read_text())
        assert native==linked and len(linked)==36 and validation['exactCallerBytes'] is True
        assert validation['linkerAttempt']['exitCode']==0 and validation['linkerSha256']=='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
        assert validation['sourceSha256']==row['sourceSha256'] and validation['sourceObjectSha256']==row['objectSha256']
        assert validation['nativeSpanSha256']==sha(native) and validation['linkedCallerSha256']==sha(linked)
        row.update(outputSha256=sha(linked),linked=False,exactBytes=36,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,
            signature='u32 '+row['name']+'(void)',oracle=dict(supported=True,cases=976,actualReturns=1952,
                report=ORACLE,reportSha256=sha((ROOT/ORACLE).read_bytes()),limits=oracle['limitations']))
        rows.append(row)
        entries[row['name']]=own
        for rel in row['relocations']:
            target=int(rel['target'],0)
            entries[rel['symbol']]=data_entry('main',target,cache) if rel['targetMode']=='data' else native_entry('main',target,cache)
    assert len(rows)==1
    for dependency in oracle['runtimeDependencies']:
        assert sha((ROOT/dependency['path']).read_bytes())==dependency['sha256']
    deps=[d['path'] for d in oracle['runtimeDependencies']]+[oracle['vectorSidecar']['path'],oracle['producerControls']['path'],controls['vectorSidecar']['path']]
    deps += [FIXTURE,CONTROL_SCRIPT,CONTROLS,'match_mechanics_save_20261031_lane_pointer_sequence.py',
        'evidence/application/save_core_controller_controls_20261031_v2.py','source_dependencies.py',
        'match_mechanics_save_20261029_record33.py','match_mechanics_save_20261029_item_use.py','provenance/seed-manifest.json',
        oracle['retainedLegacySource']['path'],'evidence/attempts/pointer-sequence-control-code-bounds-20261031.json']
    deps += [r['source'] for r in rows+controls['wholeSourceRealLinks']]+[v[0]['symbolsFile'] for v in cache.values()]
    verify_inputs()
    report=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,matches=rows,
        matchedFunctions=1,matchedBytes=36,sourceCreditAdded=0,sourceAlternativeForExistingFunction=True,
        retainedLegacySource=oracle['retainedLegacySource'],nativeSpans=oracle['nativeSpans'],
        nativeSymbolEntries=entries,nativeSymbols={n:v['address'] for n,v in entries.items()},nativeSymbolModules={n:v['module'] for n,v in entries.items()},
        sourceDependencies=[],replayDependencies=[file_identity(p) for p in sorted(set(deps))],replayRequires=[],
        oracle=dict(cases=976,actualReturns=1952,directProducerReturns=8,counts=oracle['counts'],providerKinds=0,providedCalls=0,
            nativeCaseDigest=CASE_DIGEST,reports=[r['oracle'] for r in rows],reproductionCommands=commands),
        negativeControls=dict(report=CONTROLS,sha256=sha((ROOT/CONTROLS).read_bytes()),counts=controls['counts']),
        wholeLinkedRebuild=False,registrationPerformedByThisScript=False,inputsUnchanged=True,limitations=oracle['limitations'])
    target=ROOT/'evidence/matches/mechanics-save-20261031-lane-pointer-sequence.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(functions=1,bytes=36,actualReturns=1952,producerReturns=8,sourceCreditAdded=0,reportSha256=sha(target.read_bytes()))))


if __name__=='__main__':main()
