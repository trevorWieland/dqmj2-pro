import gzip
import json
import random
import struct
import sys
from pathlib import Path
import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
from probe_battle_contracts275_20261031 import execute,OUT
from project import ROOT,configuration,now,sha256,write_json
from unicorn import __version__
ENTRY=0x021D8B4C
SOURCE=ROOT/'src/overlays/ov001_20261031_copy283/copy.c'
PINS=ROOT/'evidence/verification/ov001-copy283-inputs-20261031.json'
REPORT=ROOT/'evidence/matches/ov001-20261031-copy283.json'
WORK=ROOT/'work/ol283-proof'

def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def recipe_inputs(seed,index,destination):
    rng=random.Random(283000+seed*16+index)
    edge=[0,1,0xFFFFFFFF,0x80000000,0x7FFFFFFF,0x12345678,0x76543210,0xA17C00DE]
    words=[edge[(seed+i)%8]if seed<8 else rng.getrandbits(32)for i in range(4)]
    payload=struct.pack('<IIII',*words)
    address=0x0223161C+index*16
    output=[0,OUT,address][destination]
    initial=[(OUT-4,rng.randbytes(32)),(address,payload)]
    effects=[]if output==0 else[(output,payload[:12])]
    return dict(seed=283000+seed*16+index,entry=ENTRY,args=[index,output],initials=initial,effects=effects,expected=address,native={})

def run():
    if sys.version_info[:3]!=(3,13,5)or __version__!='2.1.4':
        raise ValueError('Copy283 pinned Python/Unicorn differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Copy283 frozen source/header/producer differs')
    config=configuration()
    if sha256(config['rom'])!=config['romSha256']:
        raise ValueError('Copy283 private input differs')
    metadata,overlay,_=measured_module('ov001')
    main_metadata,main,_=measured_module('main')
    compiler.WORK=WORK/'c'
    rows,_=compiler.compare(SOURCE,'ov001','2','off',True,thumb=False)
    if len(rows)!=1 or rows[0].get('compiledBytes')!=44:
        raise ValueError('Copy283 full44-byte compilation differs')
    row=rows[0]
    row['sourceDependencies']=[dict(path=SOURCE.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE.with_name('context.h')))]
    bindings=qualified_bindings(row)
    directory=WORK/'l'/row['objectSha256']
    proof=validate(row,bindings,directory)
    linked=(directory/'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY=WORK/'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    row.update(exactAfterGenuineLink=True,linkedMatchingBytes=44,nativeSymbolEntries=bindings)
    candidate=bytearray(overlay)
    offset=ENTRY-0x021D7240
    candidate[offset:offset+44]=linked
    if bytes(candidate)!=overlay:
        raise ValueError('Copy283 complete original/source overlay differs')
    results=[]
    summaries=[]
    for seed in range(256):
        for index in[3,11]:
            for destination in range(3):
                inputs=recipe_inputs(seed,index,destination)
                original=execute(main,overlay,**inputs)
                rebuilt=execute(main,bytes(candidate),**inputs)
                if original!=rebuilt:
                    raise ValueError('Copy283 complete original/source result differs')
                results.append(dict(seed=seed,index=index,destination=destination,result=original))
                summaries.append(dict(seed=seed,index=index,destination=destination,actualReturns=2,resultSha256=compiler.sha(encoded(original)),instructions=original['instructions'],writeTraceSha256=compiler.sha(encoded(original['writes']))))
    control=ROOT/'nonmatching/overlay-lane/20261031-copy283-null-return-negative'
    control.mkdir(parents=True,exist_ok=True)
    text=SOURCE.read_text().replace('return &native_data_ov001_0223161c[index].value;','return (Raw3 *)0;')
    if text==SOURCE.read_text():
        raise ValueError('Copy283 control mutation missing')
    for p,text in[(control/'source.c',text),(control/'context.h',SOURCE.with_name('context.h').read_text())]:
        if p.exists()and p.read_bytes()!=text.encode():
            raise ValueError('Copy283 preserve frozen control')
        p.write_bytes(text.encode())
    compiler.WORK=WORK/'negative/c'
    bad_rows,_=compiler.compare(control/'source.c','ov001','2','off',True,thumb=False)
    if len(bad_rows)!=1 or bad_rows[0].get('compileFailed'):
        raise ValueError('Copy283 control did not compile')
    bad_directory=WORK/'negative/l'
    try:
        bad_proof=validate(bad_rows[0],qualified_bindings(bad_rows[0]),bad_directory)
    except ValueError as error:
        bad_proof=error.args[0]
    if not isinstance(bad_proof,dict)or bad_proof.get('caller')!=bad_rows[0]['name']:
        raise ValueError('Copy283 control did not genuinely link')
    bad=bytearray(overlay)
    bad_bytes=(bad_directory/'caller.bin').read_bytes()
    bad[offset:offset+len(bad_bytes)]=bad_bytes
    try:
        execute(main,bytes(bad),**recipe_inputs(0,3,0))
    except ValueError as error:
        failure=error.args[0]
        if failure!='Contracts275 actual top return/frame/RAM differs':
            raise ValueError(('Copy283 unexpected control failure',failure))
    else:
        raise ValueError('Copy283 null-return control unexpectedly passed')
    raw=encoded(results)
    compressed=gzip.compress(raw,mtime=0)
    artifact=WORK/'raw-traces'/(compiler.sha(compressed)+'.json.gz')
    artifact.parent.mkdir(parents=True,exist_ok=True)
    artifact.write_bytes(compressed)
    row['oracle']=dict(supported=True,evidenceClass='Independent three-word struct copy, exact-self-alias/null destination and raw pointer return',executions=2*len(results),actualReturns=2*len(results),nativeDependencyActualReturns=0,providedCalls=0,freshMachinePerExecution=True,instructionBound=600,maximumNativeInstructions=max(r['instructions']for r in summaries),completeImageEquality=True,results=summaries,rawTraceArtifact=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=compiler.sha(compressed),bytes=len(compressed),format='json+gzip',gzipMtime=0,uncompressedSha256=compiler.sha(raw)),limitations=['Only caller-proven indices3/11; original whole-array extent and meanings remain unknown','0223161C source lies in BSS outside initialized module; all four-word records are supplied synthetic state','Destinations are null, distinct aligned12-byte writable objects or exact same source subobjects; partial-overlap/unaligned/invalid pointers are unsupported','External BSS declaration and unused fourth stride word add zero initialized-data/source credit; source struct types are minimal byte-layout views','No actor initialization, ordinary scene reachability, lifecycle or original typedef semantics established'])
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=config['romSha256'],processor='arm9',program='',module='ov001',mode='arm',moduleInputSha256=metadata['sha256'],mainInputSha256=main_metadata['sha256'],matches=[row],nativeSymbols={r['symbol']:r['target']for r in row['relocations']},isolatedLink=proof,nativeSourceBytes=44,functionMatches=1,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,rejectedNullReturn=dict(expectedRejected=True,failure=failure,compilation=bad_rows,actualLinkComparison=bad_proof,sourceCredit=0),inputPins=pins['files'],generatorSha256=sha256(__file__),limitations=['Full registry/module/ROM validation remains integrator-owned','createdUtc alone is volatile','No assembly, blobs, opcode patches, forced registers or invented input parameters'],reproductionCommand='python match_ov001_copy283_20261031.py')
    report['deterministicContentSha256']=compiler.sha(encoded({k:v for k,v in report.items()if k!='createdUtc'}))
    write_json(REPORT,report)
    print(json.dumps(dict(actualReturns=2*len(results),nativeDependencyActualReturns=0,providers=0,maximumNativeInstructions=row['oracle']['maximumNativeInstructions'])))

if __name__=='__main__':
    run()
